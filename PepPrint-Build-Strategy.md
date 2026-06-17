# PepPrint — Build Strategy & Step-by-Step Game Plan
**Created: June 14, 2026**
**Product: AI-Powered Blood Biomarker-to-Peptide Compatibility Analysis Platform**

---

## PRODUCT OVERVIEW

PepPrint analyzes blood panel data and generates personalized peptide therapy compatibility reports. Dual-sided platform: patient side (upload blood work, get report, book telemed) and provider side (PepPrint Pro — clinical dashboard).

## TECH STACK (DECIDED)

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** Rust (Axum framework) — enterprise-grade, memory-safe
- **AI Layer:** Python (LangChain, PDF parsing, biomarker extraction)
- **Database:** PostgreSQL (ACID-compliant, HIPAA-capable)
- **Infrastructure:** Alex's NAS (48TB Ubiquiti/Seagate) for production data, Vercel for frontend

## ARCHITECTURE

```
[Patient/Provider] → [React Frontend (Vercel)]
                         ↓
                    [Rust API (Axum)]
                         ↓
              ┌──────────┼──────────┐
              ↓          ↓          ↓
        [PostgreSQL]  [Python AI]  [Off-chain
         (biomarker   (analysis    encrypted storage
          database)    engine)     on NAS]
              ↓
        [Report Generation]
              ↓
        [Patient Portal / Provider Dashboard]
```

---

## PHASE 1: Biomarker Mapping Database + AI Analysis Engine (Weeks 1-2)

### Step 1: Database Schema & Biomarker Mapping Population
- Design PostgreSQL schema for biomarker-to-peptide mappings
- Populate with all core mappings from the patent (hs-CRP→BPC-157, HbA1c→GLP-1, etc.)
- Include: optimal ranges, deviation thresholds, compatibility classifications, clinical reasoning, confidence scores, contraindications
- Create admin interface for adding/editing mappings

### Step 2: Python AI Analysis Engine
- Build biomarker data intake pipeline (JSON/API input)
- Implement deterministic mapping algorithm (biomarker → database lookup → peptide match)
- Add cross-peptide analysis (multiple biomarkers pointing to same peptide = boost score)
- Add contraindication checking
- Add priority ranking algorithm
- Output: structured JSON compatibility profile

### Step 3: Testing & Validation
- Create test blood panel data sets (various biomarker combinations)
- Verify mapping accuracy against clinical literature
- Test edge cases (missing markers, extreme values, contradictory markers)
- **Show raw test output → Report to Enoch before proceeding**

---

## PHASE 2: Blood Work Upload & PDF Parsing (Weeks 2-3)

### Step 4: PDF Upload Pipeline
- Build PDF/image upload endpoint in Rust backend
- Integrate Python OCR module for lab report parsing
- Train OCR on common lab formats (Quest, LabCorp, Everlywell, LetsGetChecked)
- Build normalization layer (standardize units, map lab names to canonical identifiers)
- Build validation layer (range checking, anomaly detection, user confirmation)

### Step 5: Dual-Mode Data Handling
- Implement Mode I (identified data with PHI — HIPAA-compliant pathway)
- Implement Mode II (de-identified data with anonymous tokens)
- Build API webhook endpoint for lab partner integration
- Design data segregation between Mode I and Mode II records

### Step 6: Testing
- Test PDF parsing with real lab report samples
- Test dual-mode data flows
- Verify no Mode II data leaks into Mode I identified records
- **Show raw test output → Report to Enoch**

---

## PHASE 3: Report Generation & Patient Portal (Weeks 3-4)

### Step 7: Report Generation Module
- Transform AI analysis output into structured report format
- Build report sections: Patient Summary, Biomarker Findings, Peptide Compatibility Profile, Consultation Recommendation
- Generate PDF report output (branded, professional)
- Generate interactive web report (patient portal view)

### Step 8: Patient-Facing Frontend
- Build React + Vite patient portal
- Pages: Landing/Marketing, Upload Blood Work, View Report, Book Telemed
- Integrate Stripe for report purchase ($49-$99)
- Build user account system (auth, password reset, profile)

### Step 9: Testing & Polish
- End-to-end test: upload blood work → AI analysis → report generation → view report
- UI/UX review
- **Show complete output → Report to Enoch**

---

## PHASE 4: Provider Portal — PepPrint Pro (Weeks 4-5)

### Step 10: Provider Dashboard
- Build provider account registration and authentication
- Provider dashboard: patient list, compatibility reports, biomarker history
- Biomarker-to-peptide reference lookup tool (searchable database)
- Patient management tools

### Step 11: Telemedicine Integration
- Integrate telemed booking system
- Pre-consultation data delivery (provider sees PepPrint before consult)
- Post-consultation protocol tracking

### Step 12: Subscription & Billing
- Provider subscription management ($99-$299/month)
- Stripe integration for recurring billing
- Revenue tracking dashboard

### Step 13: Final Testing & Launch Prep
- Full end-to-end testing
- Security review
- **Pre-flight check → Show results → Report to Enoch**
- Launch readiness review

---

## BUILD PIPELINE (FOLLOW FOR EACH STEP)

1. Claude Code (DeepSeek V4 Pro proxy) builds → show raw output
2. Tests → show raw results
3. If tests fail → back to Claude Code → show corrected output
4. Pre-flight check → show results
5. Report to Enoch at each phase boundary

## KEY DEPENDENCIES

- NAS hardware delivery (June 16/22/23 — Alex's order)
- HIPAA compliance materials (Compliancy Group or similar — parallel track)
- Everlywell partnership outreach (after MVP built)
- Stripe account configuration (George has existing business entity)

## FILE LOCATIONS

- Code: `bits/pepprint/` (frontend, backend, AI engine)
- Patent: Desktop + Obsidian `patents/PepPrint-Provisional-Patent.md`
- This strategy: Desktop + Obsidian
