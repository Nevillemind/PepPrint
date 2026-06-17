"""Data models for the PepPrint AI engine."""

from typing import Optional
from pydantic import BaseModel


class BiomarkerInput(BaseModel):
    """Single biomarker input from patient data."""
    name: str
    value: float
    unit: str


class BiomarkerAnalysisRequest(BaseModel):
    """Request payload for the AI engine."""
    biomarkers: list[BiomarkerInput]


class PeptideRecommendation(BaseModel):
    """A single peptide recommendation."""
    peptide: str
    confidence: float
    evidence: list[str]
    contraindications: list[str]
    priority: int
    dosage_note: str


class BiomarkerResult(BaseModel):
    """Analysis result for a single biomarker."""
    name: str
    value: float
    unit: str
    status: str  # high, low, normal
    optimal_range: Optional[str] = None
    category: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Full analysis response from the AI engine."""
    patient_biomarkers: list[BiomarkerResult]
    recommendations: list[PeptideRecommendation]
    warnings: list[str]
    timestamp: str
