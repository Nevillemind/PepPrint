use std::env;

pub struct Config {
    pub port: u16,
    pub db_path: String,
    pub python_engine: String,
    pub stripe_secret_key: String,
    pub stripe_webhook_secret: String,
    pub base_url: String,
}

impl Config {
    pub fn from_env() -> Self {
        Config {
            port: env::var("PORT")
                .unwrap_or_else(|_| "3007".into())
                .parse()
                .unwrap_or(3007),
            db_path: env::var("DB_PATH").unwrap_or_else(|_| {
                "../data/peptides.db".into()
            }),
            python_engine: env::var("PYTHON_ENGINE").unwrap_or_else(|_| {
                "../ai-engine/engine.py".into()
            }),
            stripe_secret_key: env::var("STRIPE_SECRET_KEY")
                .unwrap_or_else(|_| "sk_test_placeholder".into()),
            stripe_webhook_secret: env::var("STRIPE_WEBHOOK_SECRET")
                .unwrap_or_else(|_| "whsec_placeholder".into()),
            base_url: env::var("BASE_URL")
                .unwrap_or_else(|_| format!("http://127.0.0.1:{}", 3007)),
        }
    }
}
