"""Biomarker database — SQLite schema creation and population."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "peptides.db"


def get_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Create all tables if they don't exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS biomarkers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            unit TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS peptides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            category TEXT,
            half_life TEXT,
            contraindications TEXT
        );

        CREATE TABLE IF NOT EXISTS biomarker_peptide_mappings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            biomarker_id INTEGER NOT NULL,
            peptide_id INTEGER NOT NULL,
            direction TEXT NOT NULL CHECK(direction IN ('high', 'low', 'normal', 'any')),
            threshold TEXT,
            clinical_reasoning TEXT NOT NULL,
            confidence_score REAL NOT NULL,
            priority INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (biomarker_id) REFERENCES biomarkers(id),
            FOREIGN KEY (peptide_id) REFERENCES peptides(id),
            UNIQUE(biomarker_id, peptide_id, direction)
        );

        CREATE TABLE IF NOT EXISTS optimal_ranges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            biomarker_id INTEGER NOT NULL UNIQUE,
            min_optimal REAL,
            max_optimal REAL,
            unit TEXT,
            source_reference TEXT,
            FOREIGN KEY (biomarker_id) REFERENCES biomarkers(id)
        );

        CREATE TABLE IF NOT EXISTS cross_peptide_boosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            primary_mapping_id INTEGER NOT NULL,
            related_mapping_id INTEGER NOT NULL,
            boost_factor REAL NOT NULL DEFAULT 1.1,
            reasoning TEXT,
            FOREIGN KEY (primary_mapping_id) REFERENCES biomarker_peptide_mappings(id),
            FOREIGN KEY (related_mapping_id) REFERENCES biomarker_peptide_mappings(id)
        );
    """)


def populate_data(conn: sqlite3.Connection) -> None:
    """Populate database with core biomarker-to-peptide mappings."""

    # ── Biomarkers ──
    biomarkers = [
        (1, "hs-CRP", "mg/L", "High-sensitivity C-reactive protein — systemic inflammation marker", "inflammatory"),
        (2, "HbA1c", "%", "Hemoglobin A1c — 3-month average blood glucose", "metabolic"),
        (3, "Fasting Insulin", "μIU/mL", "Fasting serum insulin level", "metabolic"),
        (4, "IGF-1", "ng/mL", "Insulin-like growth factor 1 — GH axis marker", "hormonal"),
        (5, "Cortisol", "μg/dL", "Primary stress hormone — HPA axis", "hormonal"),
        (6, "Testosterone", "ng/dL", "Primary androgen — HPG axis", "hormonal"),
        (7, "Collagen markers", "varies", "Collagen synthesis/degradation markers", "structural"),
        (8, "TSH", "mIU/L", "Thyroid-stimulating hormone", "hormonal"),
        (9, "Vitamin D", "ng/mL", "25-hydroxyvitamin D — immune/bone health", "nutritional"),
        (10, "ALT/AST", "U/L", "Liver enzymes — hepatocellular health", "hepatic"),
        (11, "Homocysteine", "μmol/L", "Amino acid — methylation/cardiovascular marker", "metabolic"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO biomarkers (id, name, unit, description, category) VALUES (?,?,?,?,?)",
        biomarkers,
    )

    # ── Peptides ──
    peptides = [
        (1, "BPC-157", "Gastric pentadecapeptide — tissue repair, anti-inflammatory", "repair", "~4h oral / ~2h subQ", "active cancer (angiogenic concern)"),
        (2, "KPV", "Tripeptide Lys-Pro-Val — anti-inflammatory melanocortin analog", "anti-inflammatory", "short", "none known"),
        (3, "Semaglutide", "GLP-1 receptor agonist — blood glucose / weight", "metabolic", "~7 days", "medullary thyroid carcinoma, MEN2, pancreatitis history"),
        (4, "Tirzepatide", "Dual GIP/GLP-1 receptor agonist", "metabolic", "~5 days", "medullary thyroid carcinoma, MEN2, pancreatitis history"),
        (5, "Sermorelin", "GHRH analog — stimulates pituitary GH release", "hormonal", "~12 min", "active malignancy, uncontrolled hypothyroidism"),
        (6, "CJC-1295", "Long-acting GHRH analog — sustained GH pulse", "hormonal", "~6-8 days", "active malignancy, pregnancy"),
        (7, "Ipamorelin", "Ghrelin mimetic / GHS — selective GH pulse", "hormonal", "~2h", "active cancer, pregnancy"),
        (8, "DSIP", "Delta sleep-inducing peptide — HPA/stress regulation", "neurological", "~15 min", "none established"),
        (9, "Epitalon", "Tetrapeptide — pineal regulation, telomerase activation", "longevity", "~2h", "none established"),
        (10, "HCG", "Human chorionic gonadotropin — Leydig cell stimulation", "hormonal", "~36h", "prostate cancer, pituitary adenoma"),
        (11, "Kisspeptin", "Kisspeptin-10 — GnRH pulse generator stimulator", "hormonal", "~28 min", "pregnancy, hormone-sensitive cancers"),
        (12, "GHK-Cu", "Copper tripeptide — tissue remodeling, collagen synthesis", "repair", "~1-2h", "copper toxicity (rare)"),
        (13, "Thyroid peptides", "Thyroid-specific peptide complex — thyroid support", "hormonal", "varies", "thyroid storm, hyperthyroidism (in high dose)"),
        (14, "Thymosin Alpha-1", "Thymic peptide — immune modulation", "immune", "~2h", "immunosuppressant therapy, organ transplant"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO peptides (id, name, description, category, half_life, contraindications) VALUES (?,?,?,?,?,?)",
        peptides,
    )

    # ── Optimal Ranges ──
    optimal_ranges = [
        (1, 1, 0.0, 3.0, "mg/L", "AHA/CDC 2023"),
        (2, 2, 4.0, 5.7, "%", "ADA 2024"),
        (3, 3, 2.6, 10.0, "μIU/mL", "Endocrine Society"),
        (4, 4, None, None, "ng/mL", "Age-adjusted reference ranges apply"),
        (5, 5, 6.0, 25.0, "μg/dL", "Endocrine Society"),
        (6, 6, 300, 1000, "ng/dL", "AUA 2023 (male)"),
        (7, 7, None, None, "varies", "Clinical context-dependent"),
        (8, 8, 0.4, 4.5, "mIU/L", "ATA 2023"),
        (9, 9, 30, 100, "ng/mL", "Endocrine Society"),
        (10, 10, 0, 40, "U/L", "ACG 2023"),
        (11, 11, 0, 15, "μmol/L", "AHA 2023"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO optimal_ranges (id, biomarker_id, min_optimal, max_optimal, unit, source_reference) VALUES (?,?,?,?,?,?)",
        optimal_ranges,
    )

    # ── Biomarker → Peptide Mappings ──
    mappings = [
        # hs-CRP high → BPC-157, KPV
        (1, 1, 1, "high", ">3.0 mg/L", "hs-CRP elevated → systemic inflammation → BPC-157 tissue repair", 92, 1),
        (2, 1, 2, "high", ">3.0 mg/L", "hs-CRP elevated → inflammatory modulation via KPV cascade", 88, 2),
        # HbA1c high → Semaglutide, Tirzepatide
        (3, 2, 3, "high", ">5.7%", "HbA1c elevated → insulin resistance → GLP-1 agonist Semaglutide", 95, 1),
        (4, 2, 4, "high", ">5.7%", "HbA1c elevated → dual GIP/GLP-1 → Tirzepatide metabolic regulation", 93, 2),
        # Fasting Insulin high → Semaglutide
        (5, 3, 3, "high", ">10 μIU/mL", "Fasting insulin elevated → hyperinsulinemia → GLP-1 pathway", 94, 1),
        # IGF-1 low → Sermorelin, CJC-1295, Ipamorelin
        (6, 4, 5, "low", "age-adjusted", "IGF-1 low → GH deficiency → Sermorelin GHRH analog", 91, 1),
        (7, 4, 6, "low", "age-adjusted", "IGF-1 low → GH axis stimulation → CJC-1295 long-acting GHRH", 90, 2),
        (8, 4, 7, "low", "age-adjusted", "IGF-1 low → ghrelin mimetic → Ipamorelin GH pulse", 89, 3),
        # Cortisol high → DSIP, Epitalon
        (9, 5, 8, "high", ">25 μg/dL", "Cortisol elevated → HPA axis dysregulation → DSIP sleep/endocrine", 87, 1),
        (10, 5, 9, "high", ">25 μg/dL", "Cortisol elevated → pineal regulation → Epitalon circadian", 82, 2),
        # Testosterone low → HCG, Kisspeptin
        (11, 6, 10, "low", "<300 ng/dL", "Testosterone low → Leydig cell stimulation → HCG", 88, 1),
        (12, 6, 11, "low", "<300 ng/dL", "Testosterone low → GnRH pulse generator → Kisspeptin HPG axis", 85, 2),
        # Collagen markers any → GHK-Cu
        (13, 7, 12, "any", "any deviation", "Collagen markers deviated → tissue remodeling → GHK-Cu copper peptide", 86, 1),
        # TSH high → Thyroid peptides
        (14, 8, 13, "high", ">4.5 mIU/L", "TSH elevated → hypothyroid → thyroid peptide support", 78, 1),
        # TSH low → Thyroid peptides
        (15, 8, 13, "low", "<0.4 mIU/L", "TSH low → thyroid axis → regulatory thyroid peptides", 75, 1),
        # Vitamin D low → Thymosin Alpha-1
        (16, 9, 14, "low", "<30 ng/mL", "Vitamin D low → immune modulation → Thymosin Alpha-1", 82, 1),
        # ALT/AST high → BPC-157
        (17, 10, 1, "high", ">40 U/L", "ALT/AST elevated → hepatoprotection → BPC-157 liver peptide", 85, 1),
        # Homocysteine high → Epitalon
        (18, 11, 9, "high", ">15 μmol/L", "Homocysteine elevated → methylation → Epitalon pineal peptide", 76, 1),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO biomarker_peptide_mappings (id, biomarker_id, peptide_id, direction, threshold, clinical_reasoning, confidence_score, priority) VALUES (?,?,?,?,?,?,?,?)",
        mappings,
    )

    # ── Cross-Peptide Boosts ──
    # BPC-157 boosts from hs-CRP AND ALT/AST → extra boost
    # Epitalon from Cortisol AND Homocysteine → boost
    # Semaglutide from HbA1c AND Fasting Insulin → boost
    boosts = [
        (1, 17, 1.15, "BPC-157 recommended by hs-CRP (mapping 1) boosted by ALT/AST (mapping 17)"),   # BPC-157: hs-CRP + ALT/AST
        (17, 1, 1.15, "Reverse boost: ALT/AST → BPC-157 strengthened by hs-CRP elevation"),
        (9, 18, 1.12, "Epitalon recommended by Cortisol (mapping 9) boosted by Homocysteine (mapping 18)"),  # Epitalon: Cortisol + Homocysteine
        (18, 9, 1.12, "Reverse boost: Homocysteine → Epitalon strengthened by elevated Cortisol"),
        (3, 5, 1.10, "Semaglutide recommended by HbA1c (mapping 3) boosted by Fasting Insulin (mapping 5)"),  # Semaglutide: HbA1c + Insulin
        (5, 3, 1.10, "Reverse boost: Fasting Insulin → Semaglutide strengthened by HbA1c"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO cross_peptide_boosts (primary_mapping_id, related_mapping_id, boost_factor, reasoning) VALUES (?,?,?,?)",
        boosts,
    )

    conn.commit()


def init_db() -> None:
    """Initialize the database: create schema and populate if empty."""
    conn = get_connection()
    try:
        create_schema(conn)
        # Only populate if biomarkers table is empty
        cursor = conn.execute("SELECT COUNT(*) FROM biomarkers")
        count = cursor.fetchone()[0]
        if count == 0:
            populate_data(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
