use axum::extract::{Path, State};
use axum::Json;
use serde::Deserialize;

use crate::models::*;
use crate::revenue;
use crate::state::SharedState;

#[derive(Deserialize)]
struct StripeSessionResponse {
    id: String,
    url: Option<String>,
}

/// POST /api/billing/create-checkout
/// Creates a Stripe Checkout Session via Stripe REST API and returns the URL
pub async fn create_checkout(
    State(state): State<SharedState>,
    Json(payload): Json<CreateCheckoutRequest>,
) -> Result<Json<CreateCheckoutResponse>, (axum::http::StatusCode, Json<serde_json::Value>)> {
    let (amount_cents, report_name) = match payload.report_type.as_str() {
        "single" => (9900i64, "PepPrint Single Report"),
        "annual" => (24900, "PepPrint Annual Subscription"),
        "plus" => (34900, "PepPrint Plus Report"),
        _ => {
            return Err((
                axum::http::StatusCode::BAD_REQUEST,
                Json(serde_json::json!({"error": "Invalid report_type. Use: single, annual, plus"})),
            ));
        }
    };

    let sk = &state.config.stripe_secret_key;
    let client = reqwest::Client::new();

    // Build Stripe Checkout Session via REST API (application/x-www-form-urlencoded)
    let params = [
        ("mode", "payment"),
        ("success_url", &payload.success_url),
        ("cancel_url", &payload.cancel_url),
        ("customer_email", &payload.patient_email),
        ("line_items[0][quantity]", "1"),
        ("line_items[0][price_data][currency]", "usd"),
        ("line_items[0][price_data][unit_amount]", &amount_cents.to_string()),
        ("line_items[0][price_data][product_data][name]", report_name),
    ];

    let response = match client
        .post("https://api.stripe.com/v1/checkout/sessions")
        .header("Authorization", format!("Bearer {}", sk))
        .header("Stripe-Version", "2025-06-16")
        .form(&params)
        .timeout(std::time::Duration::from_secs(15))
        .send()
        .await
    {
        Ok(r) => r,
        Err(e) => {
            tracing::error!("Stripe API request failed: {}", e);
            return Err((
                axum::http::StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({"error": format!("Stripe API error: {}", e)})),
            ));
        }
    };

    if !response.status().is_success() {
        let status = response.status().as_u16();
        let body = response.text().await.unwrap_or_default();
        tracing::error!("Stripe API error {}: {}", status, &body[..body.len().min(500)]);
        return Err((
            axum::http::StatusCode::INTERNAL_SERVER_ERROR,
            Json(serde_json::json!({"error": format!("Stripe error {}: {}", status, body)})),
        ));
    }

    let session: StripeSessionResponse = match response.json().await {
        Ok(s) => s,
        Err(e) => {
            tracing::error!("Failed to parse Stripe response: {}", e);
            return Err((
                axum::http::StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({"error": format!("Failed to parse Stripe response: {}", e)})),
            ));
        }
    };

    let session_id = session.id.clone();
    let url = session
        .url
        .unwrap_or_else(|| "https://checkout.stripe.com/pay/".to_string() + &session_id);

    // Record pending revenue split
    if let Err(e) =
        revenue::insert_revenue_split(&state.db, &session_id, amount_cents, "pending")
    {
        tracing::error!("Failed to record revenue split: {}", e);
    }

    tracing::info!(
        "Checkout session created: id={} amount={} report={}",
        session_id,
        amount_cents,
        payload.report_type
    );

    Ok(Json(CreateCheckoutResponse { url, session_id }))
}

/// GET /api/billing/status/:session_id
/// Returns payment status from revenue_splits table
pub async fn billing_status(
    State(state): State<SharedState>,
    Path(session_id): Path<String>,
) -> Json<PaymentStatus> {
    match revenue::get_revenue_split(&state.db, &session_id) {
        Some(split) => Json(PaymentStatus {
            session_id: split.session_id,
            status: split.status,
            amount_cents: Some(split.amount_cents),
            pepprint_share_cents: Some(split.pepprint_share_cents),
            everlywell_share_cents: Some(split.everlywell_share_cents),
            created_at: Some(split.created_at),
        }),
        None => Json(PaymentStatus {
            session_id,
            status: "not_found".into(),
            amount_cents: None,
            pepprint_share_cents: None,
            everlywell_share_cents: None,
            created_at: None,
        }),
    }
}
