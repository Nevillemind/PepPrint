use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct BiomarkerInput {
    pub name: String,
    pub value: f64,
    pub unit: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AnalyzeRequest {
    pub biomarkers: Vec<BiomarkerInput>,
}

// ---- Response types ----

#[derive(Debug, Serialize, Deserialize)]
pub struct BiomarkerResult {
    pub name: String,
    pub value: f64,
    pub unit: String,
    pub status: String,
    pub optimal_range: Option<String>,
    pub category: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct PeptideRecommendation {
    pub peptide: String,
    pub confidence: f64,
    pub evidence: Vec<String>,
    pub contraindications: Vec<String>,
    pub priority: i32,
    pub dosage_note: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AnalysisResponse {
    pub patient_biomarkers: Vec<BiomarkerResult>,
    pub recommendations: Vec<PeptideRecommendation>,
    pub warnings: Vec<String>,
    pub timestamp: String,
}

#[derive(Debug, Serialize)]
pub struct PeptideRow {
    pub id: i64,
    pub name: String,
    pub description: String,
    pub category: String,
    pub half_life: String,
    pub contraindications: String,
}

#[derive(Debug, Serialize)]
pub struct BiomarkerRow {
    pub id: i64,
    pub name: String,
    pub unit: String,
    pub description: String,
    pub category: String,
}

#[derive(Debug, Serialize)]
pub struct HealthCheck {
    pub status: String,
    pub version: String,
    pub db: String,
}

// ---- Stripe / Billing types ----

#[derive(Debug, Deserialize)]
pub struct CreateCheckoutRequest {
    pub report_type: String,       // "single" | "annual" | "plus"
    pub patient_email: String,
    pub success_url: String,
    pub cancel_url: String,
}

#[derive(Debug, Serialize)]
pub struct CreateCheckoutResponse {
    pub url: String,
    pub session_id: String,
}

#[derive(Debug, Serialize)]
pub struct RevenueSplitRow {
    pub id: String,
    pub session_id: String,
    pub amount_cents: i64,
    pub pepprint_share_cents: i64,
    pub everlywell_share_cents: i64,
    pub status: String,
    pub created_at: String,
}

#[derive(Debug, Serialize)]
pub struct PaymentStatus {
    pub session_id: String,
    pub status: String,
    pub amount_cents: Option<i64>,
    pub pepprint_share_cents: Option<i64>,
    pub everlywell_share_cents: Option<i64>,
    pub created_at: Option<String>,
}
