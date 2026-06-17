"""Tests for the PepPrint AI Engine."""

import json
import sys
import os

# Ensure we can import engine modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import analyze
from models import BiomarkerAnalysisRequest, BiomarkerInput


def test_hs_crp_high():
    """hs-CRP > 3.0 mg/L → should recommend BPC-157 (92) and KPV (88)."""
    req = BiomarkerAnalysisRequest(
        biomarkers=[BiomarkerInput(name="hs-CRP", value=5.2, unit="mg/L")]
    )
    resp = analyze(req)

    assert len(resp.recommendations) >= 2, f"Expected ≥2 recommendations, got {len(resp.recommendations)}"
    peptides = [r.peptide for r in resp.recommendations]

    bpc = next((r for r in resp.recommendations if r.peptide == "BPC-157"), None)
    kpv = next((r for r in resp.recommendations if r.peptide == "KPV"), None)

    assert bpc is not None, "BPC-157 not in recommendations"
    assert kpv is not None, "KPV not in recommendations"
    assert bpc.confidence >= 88, f"BPC-157 confidence {bpc.confidence} < 88"
    assert kpv.confidence >= 80, f"KPV confidence {kpv.confidence} < 80"
    assert resp.patient_biomarkers[0].status == "high"
    print("  PASS test_hs_crp_high")


def test_hba1c_high():
    """HbA1c > 5.7% → should recommend Semaglutide (95) and Tirzepatide (93)."""
    req = BiomarkerAnalysisRequest(
        biomarkers=[BiomarkerInput(name="HbA1c", value=6.4, unit="%")]
    )
    resp = analyze(req)

    sema = next((r for r in resp.recommendations if r.peptide == "Semaglutide"), None)
    tirz = next((r for r in resp.recommendations if r.peptide == "Tirzepatide"), None)

    assert sema is not None, "Semaglutide not in recommendations"
    assert tirz is not None, "Tirzepatide not in recommendations"
    assert sema.confidence >= 90, f"Semaglutide confidence {sema.confidence} < 90"
    assert tirz.confidence >= 88, f"Tirzepatide confidence {tirz.confidence} < 88"
    assert resp.patient_biomarkers[0].status == "high"
    print("  PASS test_hba1c_high")


def test_testosterone_low():
    """Testosterone < 300 ng/dL → should recommend HCG (88) and Kisspeptin (85)."""
    req = BiomarkerAnalysisRequest(
        biomarkers=[BiomarkerInput(name="Testosterone", value=220, unit="ng/dL")]
    )
    resp = analyze(req)

    hcg = next((r for r in resp.recommendations if r.peptide == "HCG"), None)
    kiss = next((r for r in resp.recommendations if r.peptide == "Kisspeptin"), None)

    assert hcg is not None, "HCG not in recommendations"
    assert kiss is not None, "Kisspeptin not in recommendations"
    assert resp.patient_biomarkers[0].status == "low"
    print("  PASS test_testosterone_low")


def test_cross_peptide_boost():
    """hs-CRP high + ALT/AST high → BPC-157 should get boosted confidence."""
    req = BiomarkerAnalysisRequest(
        biomarkers=[
            BiomarkerInput(name="hs-CRP", value=5.2, unit="mg/L"),
            BiomarkerInput(name="ALT/AST", value=85, unit="U/L"),
        ]
    )
    resp = analyze(req)

    bpc = next((r for r in resp.recommendations if r.peptide == "BPC-157"), None)
    assert bpc is not None, "BPC-157 not in recommendations"

    # With boost: base 92 * boost > 92
    assert bpc.confidence > 92, f"BPC-157 confidence {bpc.confidence} should be boosted above 92 (cross-peptide)"
    print(f"  PASS test_cross_peptide_boost (BPC-157 boosted confidence: {bpc.confidence})")


def test_multiple_metabolic():
    """HbA1c high + Fasting Insulin high → Semaglutide should get cross-boost."""
    req = BiomarkerAnalysisRequest(
        biomarkers=[
            BiomarkerInput(name="HbA1c", value=6.4, unit="%"),
            BiomarkerInput(name="Fasting Insulin", value=14.2, unit="μIU/mL"),
        ]
    )
    resp = analyze(req)

    sema = next((r for r in resp.recommendations if r.peptide == "Semaglutide"), None)
    assert sema is not None, "Semaglutide not in recommendations"
    assert sema.confidence > 94, f"Semaglutide confidence {sema.confidence} should be boosted above 94"
    print(f"  PASS test_multiple_metabolic (Semaglutide boosted: {sema.confidence})")


def test_normal_values():
    """Normal biomarker values → no high/low recommendations."""
    req = BiomarkerAnalysisRequest(
        biomarkers=[BiomarkerInput(name="hs-CRP", value=1.5, unit="mg/L")]
    )
    resp = analyze(req)
    assert resp.patient_biomarkers[0].status == "normal"
    # No high/low mappings → recommendations should be empty
    assert len(resp.recommendations) == 0, f"Expected 0 recommendations for normal, got {len(resp.recommendations)}"
    print("  PASS test_normal_values")


def test_unknown_biomarker():
    """Unknown biomarker → warning, no crash."""
    req = BiomarkerAnalysisRequest(
        biomarkers=[BiomarkerInput(name="Gobbledygook", value=99, unit="units")]
    )
    resp = analyze(req)
    assert resp.patient_biomarkers[0].status == "unknown"
    assert len(resp.warnings) >= 1, "Expected warning for unknown biomarker"
    assert len(resp.recommendations) == 0
    print("  PASS test_unknown_biomarker")


def test_comprehensive_panel():
    """Full panel: multiple biomarkers → multiple recommendations, ranked correctly."""
    req = BiomarkerAnalysisRequest(
        biomarkers=[
            BiomarkerInput(name="hs-CRP", value=5.2, unit="mg/L"),
            BiomarkerInput(name="HbA1c", value=6.4, unit="%"),
            BiomarkerInput(name="Cortisol", value=30, unit="μg/dL"),
            BiomarkerInput(name="Testosterone", value=220, unit="ng/dL"),
            BiomarkerInput(name="Vitamin D", value=19, unit="ng/mL"),
        ]
    )
    resp = analyze(req)

    assert len(resp.recommendations) >= 6, f"Expected ≥6 recommendations, got {len(resp.recommendations)}"

    # Top recommendation should have highest confidence
    for i in range(len(resp.recommendations) - 1):
        assert resp.recommendations[i].confidence >= resp.recommendations[i + 1].confidence, \
            f"Recommendations not sorted: {resp.recommendations[i].peptide} ({resp.recommendations[i].confidence}) < {resp.recommendations[i+1].peptide} ({resp.recommendations[i+1].confidence})"

    # Semaglutide should be #1 or #2 (highest raw confidence at 95)
    top3_peptides = [r.peptide for r in resp.recommendations[:3]]
    assert "Semaglutide" in top3_peptides, f"Semaglutide not in top 3: {top3_peptides}"

    # Each recommendation should have evidence, contraindications, priority
    for r in resp.recommendations:
        assert r.evidence, f"No evidence for {r.peptide}"
        assert r.priority >= 1, f"Invalid priority for {r.peptide}"
        assert r.dosage_note, f"No dosage note for {r.peptide}"

    print(f"  PASS test_comprehensive_panel ({len(resp.recommendations)} recommendations)")
    print(f"  Top 5 peptides: {[(r.peptide, r.confidence) for r in resp.recommendations[:5]]}")


def test_json_serialization():
    """Response should serialize to valid JSON."""
    req = BiomarkerAnalysisRequest(
        biomarkers=[BiomarkerInput(name="hs-CRP", value=5.2, unit="mg/L")]
    )
    resp = analyze(req)
    js = resp.model_dump_json(indent=2)
    parsed = json.loads(js)
    assert "recommendations" in parsed
    assert "patient_biomarkers" in parsed
    assert "warnings" in parsed
    assert "timestamp" in parsed
    print("  PASS test_json_serialization")


def test_cli_roundtrip():
    """Test the CLI stdin/stdout round trip."""
    import subprocess

    input_json = json.dumps({
        "biomarkers": [
            {"name": "hs-CRP", "value": 5.2, "unit": "mg/L"},
            {"name": "HbA1c", "value": 6.4, "unit": "%"},
        ]
    })

    proc = subprocess.run(
        [sys.executable, "engine.py"],
        input=input_json,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert proc.returncode == 0, f"CLI exit code {proc.returncode}: stderr={proc.stderr}"
    output = json.loads(proc.stdout)
    assert "recommendations" in output
    assert len(output["recommendations"]) >= 3  # BPC-157, KPV, Semaglutide, Tirzepatide
    print("  PASS test_cli_roundtrip")


if __name__ == "__main__":
    print("=" * 60)
    print("PepPrint AI Engine — Test Suite")
    print("=" * 60)

    tests = [
        test_hs_crp_high,
        test_hba1c_high,
        test_testosterone_low,
        test_cross_peptide_boost,
        test_multiple_metabolic,
        test_normal_values,
        test_unknown_biomarker,
        test_comprehensive_panel,
        test_json_serialization,
        test_cli_roundtrip,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  FAIL {test.__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    print(f"{'=' * 60}")

    if failed > 0:
        sys.exit(1)
