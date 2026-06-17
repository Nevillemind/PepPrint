"""PepPrint AI Engine — biomarker → peptide recommendation analysis."""

import json
import sys
from datetime import datetime, timezone
from typing import Optional

from biomarker_db import get_connection, init_db
from models import (
    BiomarkerInput,
    BiomarkerAnalysisRequest,
    BiomarkerResult,
    PeptideRecommendation,
    AnalysisResponse,
)


def evaluate_biomarker(name: str, value: float, unit: str, conn) -> dict:
    """
    Evaluate a single biomarker: look up range, determine status (high/low/normal/unknown).
    Returns a dict with biomarker info + status + optimal_range.
    """
    cursor = conn.execute(
        """SELECT b.id, b.name, b.unit, b.category, b.description,
                  o.min_optimal, o.max_optimal, o.source_reference
           FROM biomarkers b
           LEFT JOIN optimal_ranges o ON o.biomarker_id = b.id
           WHERE LOWER(b.name) = LOWER(?)""",
        (name,),
    )
    row = cursor.fetchone()

    result = {
        "name": name,
        "value": value,
        "unit": unit,
        "category": None,
        "status": "unknown",
        "optimal_range": None,
        "biomarker_id": None,
    }

    if row is None:
        result["status"] = "unknown"
        return result

    result["biomarker_id"] = row["id"]
    result["category"] = row["category"]
    min_opt = row["min_optimal"]
    max_opt = row["max_optimal"]

    if min_opt is not None and max_opt is not None:
        result["optimal_range"] = f"{min_opt}–{max_opt} {row['source_reference'] or ''}"
        if value < min_opt:
            result["status"] = "low"
        elif value > max_opt:
            result["status"] = "high"
        else:
            result["status"] = "normal"
    else:
        result["status"] = "normal"
        result["optimal_range"] = "age-adjusted / clinical context required"

    return result


def get_contraindications(peptide_id: int, conn) -> list[str]:
    """Get contraindications for a peptide."""
    cursor = conn.execute("SELECT contraindications FROM peptides WHERE id = ?", (peptide_id,))
    row = cursor.fetchone()
    if row and row["contraindications"]:
        return [c.strip() for c in row["contraindications"].split(",") if c.strip()]
    return []


def analyze(request: BiomarkerAnalysisRequest) -> AnalysisResponse:
    """
    Main analysis pipeline:
    1. Evaluate each biomarker against optimal ranges
    2. Find matching peptide mappings
    3. Apply cross-peptide boosts
    4. Rank peptides by (confidence * boost_factor)
    5. Return structured report
    """
    init_db()
    conn = get_connection()
    warnings: list[str] = []

    try:
        # Step 1: Evaluate biomarkers
        biomarker_results = []
        matched_mapping_ids = set()  # track which mapping IDs matched
        peptide_scores: dict[str, dict] = {}  # peptide_name → aggregated data

        for b in request.biomarkers:
            eval_result = evaluate_biomarker(b.name, b.value, b.unit, conn)
            biomarker_results.append(
                BiomarkerResult(
                    name=eval_result["name"],
                    value=eval_result["value"],
                    unit=eval_result["unit"],
                    status=eval_result["status"],
                    optimal_range=eval_result["optimal_range"],
                    category=eval_result["category"],
                )
            )

            # Step 2: Find matching mappings
            status = eval_result["status"]
            bid = eval_result["biomarker_id"]

            if bid is None:
                warnings.append(f"No biomarker found in database for: {b.name}")
                continue

            # Find mappings where direction matches or is 'any'
            cursor = conn.execute(
                """SELECT bpm.id, bpm.direction, bpm.threshold, bpm.clinical_reasoning,
                          bpm.confidence_score, bpm.priority,
                          p.id AS peptide_id, p.name AS peptide_name, p.half_life, p.contraindications
                   FROM biomarker_peptide_mappings bpm
                   JOIN peptides p ON p.id = bpm.peptide_id
                   WHERE bpm.biomarker_id = ?
                     AND (bpm.direction = ? OR bpm.direction = 'any')""",
                (bid, status),
            )
            mappings = cursor.fetchall()

            for m in mappings:
                matched_mapping_ids.add(m["id"])
                pep_name = m["peptide_name"]

                if pep_name not in peptide_scores:
                    peptide_scores[pep_name] = {
                        "peptide": pep_name,
                        "confidence": m["confidence_score"],
                        "max_confidence": m["confidence_score"],
                        "evidence": [m["clinical_reasoning"]],
                        "contraindications": get_contraindications(m["peptide_id"], conn),
                        "base_priority": m["priority"],
                        "mapping_ids": [m["id"]],
                        "boost_factor": 1.0,
                        "half_life": m["half_life"] or "unknown",
                    }
                else:
                    ps = peptide_scores[pep_name]
                    ps["evidence"].append(m["clinical_reasoning"])
                    ps["mapping_ids"].append(m["id"])
                    # Take best confidence and best (lowest) base priority
                    ps["confidence"] = max(ps["confidence"], m["confidence_score"])
                    ps["max_confidence"] = max(ps["max_confidence"], m["confidence_score"])
                    ps["base_priority"] = min(ps["base_priority"], m["priority"])

        # Step 3: Apply cross-peptide boosts
        for pep_name, ps in peptide_scores.items():
            for map_id in ps["mapping_ids"]:
                cursor = conn.execute(
                    """SELECT boost_factor, related_mapping_id, reasoning
                       FROM cross_peptide_boosts
                       WHERE primary_mapping_id = ?
                         AND related_mapping_id IN ({})""".format(
                        ",".join("?" for _ in matched_mapping_ids)
                    ),
                    [map_id] + list(matched_mapping_ids),
                )
                boosts = cursor.fetchall()
                for boost in boosts:
                    ps["boost_factor"] *= boost["boost_factor"]
                    # Cap boost at 1.5x to prevent runaway
                    if ps["boost_factor"] > 1.5:
                        ps["boost_factor"] = 1.5

        # Step 4: Rank peptides
        for ps in peptide_scores.values():
            ps["adjusted_confidence"] = round(ps["confidence"] * ps["boost_factor"], 1)

        ranked = sorted(peptide_scores.values(), key=lambda x: x["adjusted_confidence"], reverse=True)

        # Step 5: Build recommendations
        recommendations = []
        for i, ps in enumerate(ranked, 1):
            rec = PeptideRecommendation(
                peptide=ps["peptide"],
                confidence=ps["adjusted_confidence"],
                evidence=ps["evidence"],
                contraindications=ps["contraindications"],
                priority=i,
                dosage_note=f"Consult physician. Half-life: {ps['half_life']}.",
            )
            recommendations.append(rec)

        # Warnings for unknowns
        for br in biomarker_results:
            if br.status == "unknown":
                warnings.append(f"Unknown biomarker: {br.name} — no reference data available")

        return AnalysisResponse(
            patient_biomarkers=biomarker_results,
            recommendations=recommendations,
            warnings=warnings,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    finally:
        conn.close()


def main():
    """CLI entry point: read JSON from stdin, write JSON to stdout."""
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {e}"}))
        sys.exit(1)

    try:
        request = BiomarkerAnalysisRequest.model_validate(data)
    except Exception as e:
        print(json.dumps({"error": f"Validation error: {e}"}))
        sys.exit(1)

    response = analyze(request)
    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
