use std::sync::Arc;
use crate::config::Config;
use crate::db::DbPool;

pub struct AppState {
    pub db: DbPool,
    pub config: Config,
}

pub type SharedState = Arc<AppState>;
