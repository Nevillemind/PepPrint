use axum::body::Bytes;
use axum::extract::State;
use axum::http::{HeaderMap, StatusCode};
use axum::response::IntoResponse;
use serde::Deserialize;

use crate::revenue;
use crate::state::{AppState, SharedState};

/// Simplified Stripe event for webhook processing
#[derive(Deserialize, Debug)]
struct StripeEvent {
    #[serde(rename = "type")]
    event_type: String,
    #[serde(default)]
    id: String,
    data: StripeEventData,
}

#[derive(Deserialize, Debug)]
struct StripeEventData {
    object: serde_json::Value,
}

/// POST /api/billing/webhook
/// Accepts Stripe webhook events, verifies signature, and processes payment events
pub async fn stripe_webhook(
    State(state): State<SharedState>,
    headers: HeaderMap,
    body: Bytes,
) -> impl IntoResponse {
    let signature = headers
        .get("stripe-signature")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("");

    let whsec = &state.config.stripe_webhook_secret;

    // Verify webhook signature (skip if using placeholder in dev)
    if whsec != "whsec_placeholder" && !verify_stripe_signature(whsec, signature, &body) {
        tracing::error!("Webhook signature verification failed");
        return (StatusCode::BAD_REQUEST, "Signature verification failed").into_response();
    }

    // Parse the event JSON
    let event: StripeEvent = match serde_json::from_slice(&body) {
        Ok(ev) => ev,
        Err(e) => {
            tracing::error!("Failed to parse webhook body: {}", e);
            return (StatusCode::BAD_REQUEST, format!("Invalid JSON: {}", e)).into_response();
        }
    };

    tracing::info!(
        "Webhook received: type={} id={}",
        event.event_type,
        event.id
    );

    match event.event_type.as_str() {
        "checkout.session.completed" => {
            let obj = &event.data.object;

            // Extract session_id and amount from the checkout session object
            let session_id = obj["id"].as_str().unwrap_or("unknown").to_string();
            let amount_cents = obj["amount_total"].as_i64().unwrap_or(0);

            tracing::info!(
                "Checkout session completed: id={} amount={}",
                session_id,
                amount_cents
            );

            // Update revenue split to completed
            if let Err(e) =
                revenue::update_revenue_status(&state.db, &session_id, "completed")
            {
                tracing::error!(
                    "Failed to update revenue split for session {}: {}",
                    session_id,
                    e
                );
            } else {
                tracing::info!(
                    "Revenue split marked completed for session {}",
                    session_id
                );
            }

            // Trigger report generation via internal API call
            trigger_report_generation(&state).await;
        }
        "payment_intent.succeeded" => {
            let pi_id = event.data.object["id"]
                .as_str()
                .unwrap_or("unknown");
            tracing::info!("Payment intent succeeded: id={}", pi_id);
        }
        "payment_intent.payment_failed" => {
            let pi_id = event.data.object["id"]
                .as_str()
                .unwrap_or("unknown");
            let error = &event.data.object["last_payment_error"];
            tracing::warn!(
                "Payment intent failed: id={} error={:?}",
                pi_id,
                error
            );
        }
        other => {
            tracing::debug!("Unhandled webhook event type: {}", other);
        }
    }

    (StatusCode::OK, "{}").into_response()
}

/// Verify Stripe webhook signature using HMAC-SHA256
///
/// Stripe signs webhooks with: t=timestamp,v1=HMAC_SHA256(secret, "timestamp.body")
fn verify_stripe_signature(secret: &str, signature_header: &str, payload: &[u8]) -> bool {
    use hmac::Mac;
    use sha2::Sha256;

    // Parse signature header: "t=1234567890,v1=abcdef,v0=..."  
    let mut timestamp = None;
    let mut v1_sig = None;

    for part in signature_header.split(',') {
        let part = part.trim();
        if let Some(t) = part.strip_prefix("t=") {
            timestamp = Some(t);
        } else if let Some(s) = part.strip_prefix("v1=") {
            v1_sig = Some(s);
        }
    }

    let (Some(ts), Some(expected_sig)) = (timestamp, v1_sig) else {
        tracing::warn!("Stripe signature header missing t= or v1=");
        return false;
    };

    // Construct the signed payload: "timestamp.payload"
    let signed_payload = format!("{}.{}", ts, String::from_utf8_lossy(payload));

    // HMAC-SHA256(secret, signed_payload)
    let mut mac = <hmac::Hmac<Sha256> as Mac>::new_from_slice(secret.as_bytes())
        .expect("HMAC can take key of any size");
    mac.update(signed_payload.as_bytes());
    let result = mac.finalize();
    let computed_sig = hex::encode(result.into_bytes());

    computed_sig == expected_sig
}

/// Trigger report generation by calling the internal analyze endpoint
async fn trigger_report_generation(state: &AppState) {
    let base_url = &state.config.base_url;
    let url = format!("{}/api/analyze", base_url);

    tracing::info!("Triggering report generation at {}", url);

    let client = reqwest::Client::new();
    match client
        .post(&url)
        .header("Content-Type", "application/json")
        .json(&serde_json::json!({"biomarkers": []}))
        .timeout(std::time::Duration::from_secs(30))
        .send()
        .await
    {
        Ok(resp) => {
            let status = resp.status();
            match resp.text().await {
                Ok(body) => {
                    tracing::info!(
                        "Report generation triggered: status={} body={}",
                        status,
                        &body[..body.len().min(500)]
                    );
                }
                Err(e) => {
                    tracing::error!("Failed to read report generation response: {}", e);
                }
            }
        }
        Err(e) => {
            tracing::error!("Failed to trigger report generation: {}", e);
        }
    }
}
