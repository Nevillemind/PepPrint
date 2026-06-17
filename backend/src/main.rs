mod config;
mod db;
mod handlers;
mod models;
mod revenue;
mod state;
mod stripe_handler;
mod webhook;

use axum::{Router, routing::get, routing::post};
use std::sync::Arc;
use tower_http::cors::{CorsLayer, Any};
use tracing_subscriber;

use config::Config;
use db::DbPool;
use state::{AppState, SharedState};
use handlers::{analyze, health_check, list_biomarkers, list_peptides};
use stripe_handler::{billing_status, create_checkout};
use webhook::stripe_webhook;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let config = Config::from_env();
    let db = DbPool::new(&config.db_path).expect("Failed to open database");

    let port = config.port;
    let state: SharedState = Arc::new(AppState { db, config });

    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let app = Router::new()
        .route("/api/health", get(health_check))
        .route("/api/peptides", get(list_peptides))
        .route("/api/biomarkers", get(list_biomarkers))
        .route("/api/analyze", post(analyze))
        // Stripe billing routes
        .route("/api/billing/create-checkout", post(create_checkout))
        .route("/api/billing/webhook", post(stripe_webhook))
        .route("/api/billing/status/{session_id}", get(billing_status))
        .layer(cors)
        .with_state(state);

    let addr = format!("127.0.0.1:{}", port);
    tracing::info!("PepPrint API listening on {}", addr);

    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
