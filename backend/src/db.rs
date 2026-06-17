use rusqlite::Connection;
use std::path::PathBuf;
use std::sync::Mutex;

/// Thread-safe database wrapper
pub struct DbPool {
    pub conn: Mutex<Connection>,
}

impl DbPool {
    pub fn new(db_path: &str) -> Result<Self, rusqlite::Error> {
        let path: PathBuf = db_path.into();
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent).ok();
        }

        let conn = Connection::open(&path)?;
        conn.execute_batch("PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL;")?;

        let pool = DbPool {
            conn: Mutex::new(conn),
        };
        pool.init_tables()?;
        Ok(pool)
    }

    fn init_tables(&self) -> Result<(), rusqlite::Error> {
        let conn = self.conn.lock().unwrap();
        conn.execute_batch(
            "CREATE TABLE IF NOT EXISTS revenue_splits (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                amount_cents INTEGER NOT NULL,
                pepprint_share_cents INTEGER NOT NULL,
                everlywell_share_cents INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT (datetime('now'))
            );"
        )?;
        tracing::info!("Database tables initialized");
        Ok(())
    }
}
