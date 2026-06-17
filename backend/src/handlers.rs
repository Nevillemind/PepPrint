use axum::extract::State;
use axum::Json;
use std::process::Command;

use crate::models::*;
use crate::state::SharedState;

/// POST /api/analyze — forward biomarker data to Python engine, return analysis
pub async fn analyze(
    State(state): State<SharedState>,
    Json(payload): Json<AnalyzeRequest>,
) -> Json<AnalysisResponse> {
    let input_json = serde_json::to_string(&payload).unwrap_or_default();

    // Determine python executable path
    let python = std::env::var("PYTHON_BIN").unwrap_or_else(|_| "python3".into());
    let engine_path = &state.config.python_engine;

    let result = Command::new(&python)
        .arg(engine_path)
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .stderr(std::process::Stdio::piped())
        .spawn();

    match result {
        Ok(mut child) => {
            use std::io::Write;
            if let Some(mut stdin) = child.stdin.take() {
                let _ = stdin.write_all(input_json.as_bytes());
            }

            let output = match child.wait_with_output() {
                Ok(o) => o,
                Err(e) => {
                    return Json(AnalysisResponse {
                        patient_biomarkers: vec![],
                        recommendations: vec![],
                        warnings: vec![format!("Failed to read Python output: {}", e)],
                        timestamp: chrono_now(),
                    })
                }
            };
            let stdout = String::from_utf8_lossy(&output.stdout);

            match serde_json::from_str::<AnalysisResponse>(&stdout) {
                Ok(resp) => Json(resp),
                Err(e) => {
                    let stderr = String::from_utf8_lossy(&output.stderr);
                    Json(AnalysisResponse {
                        patient_biomarkers: vec![],
                        recommendations: vec![],
                        warnings: vec![format!(
                            "Python engine error: {}. stderr: {}",
                            e, stderr
                        )],
                        timestamp: chrono_now(),
                    })
                }
            }
        }
        Err(e) => Json(AnalysisResponse {
            patient_biomarkers: vec![],
            recommendations: vec![],
            warnings: vec![format!("Failed to spawn Python engine: {}", e)],
            timestamp: chrono_now(),
        }),
    }
}

/// GET /api/peptides — list all peptides
pub async fn list_peptides(State(state): State<SharedState>) -> Json<Vec<PeptideRow>> {
    let conn = state.db.conn.lock().unwrap();
    let mut stmt = conn
        .prepare("SELECT id, name, description, category, half_life, contraindications FROM peptides ORDER BY id")
        .unwrap();

    let rows = stmt
        .query_map([], |row| {
            Ok(PeptideRow {
                id: row.get::<_, i64>(0)?,
                name: row.get::<_, String>(1)?,
                description: row.get::<_, String>(2)?,
                category: row.get::<_, String>(3)?,
                half_life: row.get::<_, String>(4)?,
                contraindications: row.get::<_, String>(5)?,
            })
        })
        .unwrap()
        .filter_map(|r| r.ok())
        .collect();

    Json(rows)
}

/// GET /api/biomarkers — list all biomarkers
pub async fn list_biomarkers(State(state): State<SharedState>) -> Json<Vec<BiomarkerRow>> {
    let conn = state.db.conn.lock().unwrap();
    let mut stmt = conn
        .prepare("SELECT id, name, unit, description, category FROM biomarkers ORDER BY id")
        .unwrap();

    let rows = stmt
        .query_map([], |row| {
            Ok(BiomarkerRow {
                id: row.get::<_, i64>(0)?,
                name: row.get::<_, String>(1)?,
                unit: row.get::<_, String>(2)?,
                description: row.get::<_, String>(3)?,
                category: row.get::<_, String>(4)?,
            })
        })
        .unwrap()
        .filter_map(|r| r.ok())
        .collect();

    Json(rows)
}

/// GET /api/health — health check
pub async fn health_check(State(state): State<SharedState>) -> Json<HealthCheck> {
    let db_status = match state.db.conn.lock() {
        Ok(conn) => match conn.execute_batch("SELECT 1") {
            Ok(_) => "connected".into(),
            Err(e) => format!("error: {}", e),
        },
        Err(e) => format!("lock error: {}", e),
    };

    Json(HealthCheck {
        status: "ok".into(),
        version: "0.1.0".into(),
        db: db_status,
    })
}

fn chrono_now() -> String {
    // Simple UTC timestamp without chrono crate
    std::process::Command::new("date")
        .args(["-u", "+%Y-%m-%dT%H:%M:%S.%3NZ"])
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .unwrap_or_else(|_| "unknown".into())
}
