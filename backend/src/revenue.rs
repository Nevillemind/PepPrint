use crate::db::DbPool;
use crate::models::RevenueSplitRow;
use uuid::Uuid;

/// Insert a revenue split record (60/40 PepPrint/Everlywell)
pub fn insert_revenue_split(
    db: &DbPool,
    session_id: &str,
    amount_cents: i64,
    status: &str,
) -> Result<(), rusqlite::Error> {
    let conn = db.conn.lock().unwrap();
    let id = Uuid::new_v4().to_string();
    let pepprint_share = (amount_cents as f64 * 0.6).round() as i64;
    let everlywell_share = amount_cents - pepprint_share;

    conn.execute(
        "INSERT INTO revenue_splits (id, session_id, amount_cents, pepprint_share_cents, everlywell_share_cents, status)
         VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
        rusqlite::params![id, session_id, amount_cents, pepprint_share, everlywell_share, status],
    )?;

    tracing::info!(
        "Revenue split recorded: session={} amount={} pepprint={} everlywell={} status={}",
        session_id, amount_cents, pepprint_share, everlywell_share, status
    );
    Ok(())
}

/// Update the status of a revenue split (e.g. on payment failure)
pub fn update_revenue_status(
    db: &DbPool,
    session_id: &str,
    status: &str,
) -> Result<(), rusqlite::Error> {
    let conn = db.conn.lock().unwrap();
    conn.execute(
        "UPDATE revenue_splits SET status = ?1 WHERE session_id = ?2",
        rusqlite::params![status, session_id],
    )?;
    Ok(())
}

/// Query revenue splits by session_id
pub fn get_revenue_split(db: &DbPool, session_id: &str) -> Option<RevenueSplitRow> {
    let conn = db.conn.lock().unwrap();
    let mut stmt = conn
        .prepare(
            "SELECT id, session_id, amount_cents, pepprint_share_cents, everlywell_share_cents, status, created_at
             FROM revenue_splits WHERE session_id = ?1 ORDER BY created_at DESC LIMIT 1",
        )
        .ok()?;

    stmt.query_row(rusqlite::params![session_id], |row| {
        Ok(RevenueSplitRow {
            id: row.get(0)?,
            session_id: row.get(1)?,
            amount_cents: row.get(2)?,
            pepprint_share_cents: row.get(3)?,
            everlywell_share_cents: row.get(4)?,
            status: row.get(5)?,
            created_at: row.get(6)?,
        })
    })
    .ok()
}
