# PROVISIONAL PATENT APPLICATION
## United States Patent and Trademark Office

**Title of Invention:**
System and Method for AI-Driven Blood Biomarker Analysis and Peptide Therapy Compatibility Assessment with Dual-Mode Data Handling Architecture

**Inventor:**
George Mundin
Richmond, Virginia, United States

**Correspondence Address:**
George Mundin
3900 Westerre Parkway, Suite 300
Richmond, Virginia 23233
United States

**Entity Type:** Micro-Entity

**Filing Date:** June 2026

---

> *This application claims the benefit of priority under 35 U.S.C. § 119(e) as a Provisional Patent Application. This document constitutes the full specification and technical disclosure sufficient to establish a priority date for the described invention.*

---

## SPECIFICATION

---

### TITLE OF THE INVENTION

**System and Method for AI-Driven Blood Biomarker Analysis and Peptide Therapy Compatibility Assessment with Dual-Mode Data Handling Architecture**

*Alternative Titles:*
- Artificial Intelligence Platform for Personalized Peptide Therapy Selection Based on Blood Panel Biomarker Analysis
- Dual-Mode Biomarker Intelligence System for Mapping Blood Work Results to Therapeutic Peptide Recommendations
- Computer-Implemented Method for Generating Personalized Peptide Compatibility Reports from Laboratory Blood Test Data

---

### FIELD OF THE INVENTION

The present invention relates generally to artificial intelligence systems for personalized health analysis, and more particularly to a system that:

(a) Receives blood panel biomarker data from laboratory sources, including at-home finger-prick test kits, clinical laboratory results, and provider-ordered blood panels;

(b) Operates in a dual-mode data handling architecture, supporting both identified (HIPAA-compliant) and de-identified (HIPAA Safe Harbor) data processing modes;

(c) Analyzes said biomarker data using an artificial intelligence engine that maps specific blood markers to therapeutic peptide candidates using a proprietary biomarker-to-peptide compatibility database;

(d) Generates personalized peptide compatibility reports indicating which peptide therapies may benefit the patient based on their specific biomarker profile;

(e) Integrates with telemedicine consultation platforms to enable data-driven therapeutic peptide prescribing; and

(f) Tracks biomarker changes over time to enable measurable, quantifiable assessment of therapeutic peptide protocol effectiveness.

---

### BACKGROUND OF THE INVENTION

#### 1. The Peptide Therapy Prescription Gap

Peptide therapeutics represent one of the fastest-growing segments of the global pharmaceutical market, projected to reach $87.21 billion by 2035. Peptides — short chains of amino acids that signal cells to perform specific biological functions — have demonstrated therapeutic efficacy across a wide range of health domains including weight loss (GLP-1 agonists such as semaglutide and tirzepatide), tissue repair and recovery (BPC-157, TB-500), anti-aging and collagen synthesis (GHK-Cu), gut health (BPC-157, KPV), hormone optimization (sermorelin, CJC-1295), immune modulation (thymosin alpha-1), cognitive enhancement (dihexa, cerebrolysin), and sleep optimization (DSIP, epitalon).

Despite this therapeutic potential, the current standard of care in peptide therapy prescribing suffers from a critical deficiency: peptide selection is based almost entirely on symptomatic assessment rather than objective biomarker data. The typical prescribing workflow consists of:

1. Patient describes symptoms in plain language during a telemedicine or in-person consultation;
2. Provider asks qualitative questions about the patient's health concerns (e.g., "Do you have gut issues?" "Joint pain?" "Trouble sleeping?" "Want to lose weight?");
3. Provider selects a peptide based on the patient's self-reported symptoms and the provider's clinical experience;
4. No blood work is required, reviewed, or analyzed prior to peptide selection in the majority of telemedicine peptide prescribing encounters.

This symptom-based approach has significant limitations:

**Lack of Personalization:** Two patients reporting "fatigue and joint pain" may receive identical peptide recommendations despite having fundamentally different underlying biomarker profiles. One patient's fatigue may stem from metabolic dysfunction (elevated HbA1c, insulin resistance) while another's may result from hormonal deficiency (low testosterone, elevated cortisol). Without blood work analysis, these distinctions are invisible to the prescribing provider.

**No Baseline Measurement:** Without pre-treatment biomarker data, there is no objective baseline against which to measure peptide therapy effectiveness. "I feel better" is not a clinical outcome. True therapeutic assessment requires quantifiable before-and-after biomarker comparison.

**No Systematic Biomarker-to-Peptide Mapping:** The connection between specific blood markers and specific therapeutic peptides exists only in the individual knowledge of prescribing providers. There is no standardized, systematic, database-driven mapping that connects biomarker deviations to peptide therapy candidates.

**Low Conversion Rates:** Telemedicine peptide consultations that rely solely on symptom discussion have lower patient conversion rates because the patient has no objective evidence that the recommended peptide addresses their specific biological needs.

#### 2. The Data Accessibility Problem

Millions of consumers obtain blood work annually through annual physical examinations, workplace wellness programs, at-home test kits (Everlywell, LetsGetChecked, Quest Direct, HealthLabs), and direct-to-consumer lab services. This blood panel data contains valuable biomarker information — including inflammatory markers (hs-CRP, cytokines), metabolic markers (HbA1c, insulin, glucose), hormonal markers (testosterone, estradiol, cortisol, thyroid panels), growth factors (IGF-1), nutritional markers (vitamin D, B12, iron), and other measurable indicators of physiological function.

However, this data is:

(a) Siloed in individual laboratory portals, electronic health record systems, and proprietary platforms;
(b) Rarely analyzed beyond simple "normal/abnormal" flagging against population reference ranges;
(c) Never mapped to specific therapeutic intervention recommendations by an automated system;
(d) Not made available to patients in a format that connects their biomarker data to actionable health optimization strategies;
(e) Not tracked longitudinally in a systematic, automated fashion for therapeutic protocol optimization.

There exists a critical need for a system that can receive blood panel biomarker data, analyze it using AI to identify therapeutic peptide candidates, and generate personalized compatibility reports that drive informed telemedicine consultations.

#### 3. The HIPAA Compliance Spectrum

Health Insurance Portability and Accountability Act (HIPAA) regulations govern the handling of Protected Health Information (PHI) in the United States. Any system that processes patient health data must either:

(a) Operate as a Covered Entity or Business Associate with full HIPAA compliance — requiring administrative safeguards (policies, training, risk assessments), physical safeguards (facility access controls, device security), and technical safeguards (encryption, access controls, audit logging); or

(b) Process only de-identified data that has been stripped of the 18 identifiers specified under the HIPAA Safe Harbor method (45 CFR §164.514(b)), rendering the data no longer classified as PHI and therefore not subject to HIPAA regulation.

Existing health AI platforms are forced to choose one of these modes. Systems that handle identified data bear the full cost and complexity of HIPAA compliance. Systems that use de-identified data cannot re-identify patients or operate in a direct clinical workflow.

There exists a need for a system architecture that supports BOTH modes simultaneously — operating with identified data when the operating entity has achieved HIPAA compliance, AND operating with de-identified data when partnering with laboratory services that perform de-identification before data transmission. This dual-mode flexibility enables the system to operate in diverse deployment scenarios ranging from fully HIPAA-compliant standalone installations to partner-integrated de-identified workflows.

---

### SUMMARY OF THE INVENTION

The present invention provides a system and method for AI-driven analysis of blood biomarker data and generation of personalized peptide therapy compatibility reports. The system comprises:

(a) A **Biomarker Data Intake Module** capable of receiving blood panel results in both identified (PHI) and de-identified formats, supporting multiple input methods including API webhooks from laboratory partners, PDF/document upload with optical character recognition (OCR), manual entry, and structured data file import;

(b) A **Dual-Mode Data Handling Architecture** that enables the system to operate in:
   - Mode I: Identified data mode, wherein the system receives and processes PHI in full compliance with HIPAA regulations, maintaining all required administrative, physical, and technical safeguards;
   - Mode II: De-identified data mode, wherein the system receives biomarker values that have been de-identified according to HIPAA Safe Harbor or Expert Determination method, with no patient identifiers attached;
   - Said system may operate in either mode or both modes simultaneously depending on the deployment configuration and compliance status of the operating entity;

(c) A **Biomarker-to-Peptide Mapping Database** containing proprietary mappings between blood biomarkers and therapeutic peptide candidates, including:
   - Biomarker deviation thresholds (optimal ranges, not merely normal ranges);
   - Directional indicators (elevated vs. deficient);
   - Peptide compatibility classifications (High, Medium, Low);
   - Clinical reasoning for each mapping;
   - Confidence scoring based on evidence strength;

(d) An **AI Analysis Engine** that processes received biomarker data through said mapping database, generating a personalized peptide compatibility profile for each set of blood panel results;

(e) A **Report Generation Module** that transforms the analysis output into a structured peptide compatibility report comprising biomarker findings, peptide compatibility classifications, clinical reasoning, and telemedicine consultation recommendations;

(f) A **Longitudinal Tracking Module** that stores sequential biomarker data sets and generates before-and-after comparison analyses to quantify therapeutic peptide protocol effectiveness over time;

(g) A **Provider Portal** enabling healthcare providers to view patient compatibility reports, access the biomarker-to-peptide mapping database with clinical references, and manage patient caseloads through a secured dashboard;

(h) A **Telemedicine Integration Layer** facilitating seamless referral from compatibility report to telemedicine consultation, enabling data-driven peptide prescribing.

---

### BRIEF DESCRIPTION OF THE DRAWINGS

**Figure 1:** System architecture diagram showing the dual-mode data handling architecture, with identified data pathway (HIPAA-compliant) and de-identified data pathway (Safe Harbor), both feeding into the AI Analysis Engine.

**Figure 2:** Biomarker data intake workflow showing multiple input channels (laboratory API webhook, PDF upload with OCR, manual entry, structured file import) and the dual-mode preprocessing layer.

**Figure 3:** Biomarker-to-Peptide Mapping Database structure showing the relationship between biomarkers, deviation thresholds, peptide candidates, compatibility classifications, and clinical reasoning.

**Figure 4:** AI Analysis Engine processing flow showing biomarker data input, mapping database lookup, compatibility scoring algorithm, and report output generation.

**Figure 5:** Patient-side user experience flow showing blood test kit ordering, results upload, PepPrint report generation, and telemedicine consultation booking.

**Figure 6:** Provider portal (PepPrint Pro) dashboard layout showing patient list, individual compatibility reports, biomarker history timeline, and peptide protocol tracking.

**Figure 7:** Longitudinal tracking module showing before-and-after biomarker comparison with delta calculations and therapeutic effectiveness scoring.

**Figure 8:** Dual-mode deployment architectures — (A) HIPAA-compliant standalone deployment with identified data, (B) Partner-integrated deployment with laboratory-side de-identification, (C) Hybrid deployment supporting both modes.

**Figure 9:** Telemedicine integration workflow showing PepPrint report delivery to provider, pre-consultation data review, consultation conduct, and post-consultation protocol tracking.

**Figure 10:** Revenue and billing flow showing patient-side payment processing, provider subscription management, and laboratory partner revenue sharing.

---

### DETAILED DESCRIPTION OF THE INVENTION

---

#### COMPONENT A: Biomarker Data Intake Module

The Biomarker Data Intake Module is the entry point for all blood panel data into the system. It supports multiple input channels to accommodate diverse deployment scenarios:

**A1. Laboratory API Webhook:** A RESTful API endpoint capable of receiving structured biomarker data from laboratory information systems, at-home testing kit providers (including but not limited to Everlywell, LetsGetChecked, Quest Diagnostics, LabCorp, HealthLabs, Rupa Health, and Fullscript), and electronic health record (EHR) systems via HL7/FHIR standards. The webhook accepts JSON payloads containing biomarker values, reference ranges, units of measurement, test dates, and optional patient identifiers. The API supports both identified transmissions (with PHI, requiring BAA) and de-identified transmissions (with anonymous patient tokens only).

**A2. PDF/Document Upload with OCR:** A document processing pipeline that accepts blood panel results in PDF, JPEG, PNG, or other image formats. The pipeline employs optical character recognition (OCR) to extract biomarker names, values, units, and reference ranges from laboratory-issued documents. The OCR engine is specifically trained on common laboratory report formats, including those produced by major reference laboratories (Quest, LabCorp, Everlywell, LetsGetChecked) and standard CMS-1500 laboratory encounter forms. Extracted data is validated against known biomarker formats and presented to the user for confirmation before processing.

**A3. Manual Entry Interface:** A structured data entry form allowing patients or providers to manually input biomarker values from physical laboratory reports. The form includes validation rules (range checking, unit normalization, required field enforcement) and supports all standard blood panel biomarkers.

**A4. Structured Data File Import:** Support for importing biomarker data from structured file formats including CSV, JSON, XML, and industry-standard health data formats (HL7 FHIR resources, CCD/CCDA documents).

**Data Normalization:** All intake channels feed into a normalization layer that:
- Converts all biomarker values to standardized units (e.g., mg/dL, ng/mL, mIU/L);
- Maps laboratory-specific biomarker names to canonical identifiers (e.g., "High Sensitivity C-Reactive Protein" and "hs-CRP" and "CRP, High Sensitivity" all map to the same canonical biomarker);
- Validates values against physiological plausibility ranges;
- Flags missing or anomalous values for review;
- Timestamps all data with UTC recording.

---

#### COMPONENT B: Dual-Mode Data Handling Architecture

The Dual-Mode Data Handling Architecture is a core novelty of the present invention. Unlike existing health AI platforms that are architecturally locked into either identified (HIPAA-compliant) or de-identified data processing, the present invention supports both modes within a single system architecture.

**Mode I — Identified Data Mode (HIPAA-Compliant):**

In Mode I, the system receives Protected Health Information (PHI) directly from patients, providers, or laboratory partners. In this mode, the system:

(a) Maintains full HIPAA compliance including:
   - AES-256 encryption for all data at rest;
   - TLS 1.3 for all data in transit;
   - Role-based access controls with unique user authentication;
   - Comprehensive audit logging of all PHI access (who, what, when);
   - Automatic session logoff after configurable inactivity periods;
   - Designated Security Officer and Privacy Officer roles;
   - Documented incident response and breach notification procedures;
   - Annual risk assessments and workforce training;

(b) Associates biomarker data with patient identity records, enabling:
   - Direct patient-facing report delivery;
   - Provider access to identified patient reports;
   - Longitudinal tracking under patient identity;
   - Telemedicine consultation with full clinical context;

(c) Maintains Business Associate Agreements (BAAs) with all vendors that touch PHI, including AI API providers, cloud hosting providers, and laboratory partners.

**Mode II — De-Identified Data Mode (Safe Harbor):**

In Mode II, the system receives biomarker data that has been de-identified by the source laboratory before transmission. In this mode:

(a) The laboratory partner performs de-identification according to the HIPAA Safe Harbor method, removing all 18 specified identifiers (45 CFR §164.514(b)(2)) and replacing them with an anonymous patient token;

(b) The system receives only:
   - An anonymous patient token (e.g., "EVL-7842-XK39");
   - Biomarker values and units;
   - Test date;
   - No name, date of birth, address, phone, email, SSN, or any other identifier;

(c) The system processes the de-identified biomarker data through the AI Analysis Engine identically to Mode I;

(d) The generated compatibility report is returned to the laboratory partner via API, tagged with the same anonymous patient token;

(e) The laboratory partner re-identifies the report on their side and delivers it to the patient through their HIPAA-compliant patient portal;

(f) Because the system never receives PHI, HIPAA compliance is not required for the analysis engine itself, though a BAA may still be executed as a best practice.

**Simultaneous Dual-Mode Operation:**

The system architecture supports simultaneous operation in both modes. For example:
- The system may receive de-identified data from a laboratory partner (Mode II) while also receiving identified data directly from a provider who has uploaded blood work through the Provider Portal (Mode I);
- Mode I and Mode II data are processed by the same AI Analysis Engine using the same biomarker-to-peptide mapping database;
- Mode I data includes patient identity for direct report delivery;
- Mode II data uses anonymous tokens for partner-mediated report delivery;
- The system maintains strict segregation between Mode I identified records and Mode II anonymous records.

**This dual-mode architecture is a novel contribution not found in existing health AI platforms.** It enables the system to operate in diverse commercial configurations — from fully compliant standalone deployments to lightweight partner-integrated workflows — without requiring architectural changes or separate codebases.

---

#### COMPONENT C: Biomarker-to-Peptide Mapping Database

The Biomarker-to-Peptide Mapping Database is the proprietary core intellectual property of the present invention. It contains structured mappings between blood biomarkers and therapeutic peptide candidates.

**Database Structure:**

Each mapping record comprises:

1. **Biomarker Identifier:** Canonical name and LOINC code (e.g., hs-CRP, LOINC 30522-7);
2. **Deviation Direction:** Elevated, Deficient, or Abnormal (any direction);
3. **Optimal Range:** The system uses optimal ranges (not merely "normal" population ranges) based on functional medicine and longevity research. For example:
   - hs-CRP: Optimal < 1.0 mg/L (normal is < 3.0 mg/L);
   - HbA1c: Optimal < 5.4% (normal is < 5.7%);
   - IGF-1: Optimal varies by age, maintained in age-stratified reference tables;
   - Vitamin D: Optimal 50-70 ng/mL (normal is > 20 ng/mL);
4. **Deviation Threshold:** Value ranges triggering peptide compatibility classification (High/Medium/Low);
5. **Mapped Peptide Candidate(s):** One or more therapeutic peptides indicated for the detected biomarker deviation;
6. **Compatibility Classification:** High (strong evidence), Medium (moderate evidence), Low (emerging evidence);
7. **Clinical Reasoning:** Textual explanation of the biomarker-to-peptide connection, citing mechanism of action and therapeutic rationale;
8. **Evidence Strength:** Confidence score (1-10) based on available clinical evidence, animal studies, and mechanistic plausibility;
9. **Contraindication Flags:** Known contraindications, drug interactions, or caution indicators;

**Core Biomarker-to-Peptide Mappings (Representative, Not Exhaustive):**

| Biomarker | Deviation | Optimal Range | Mapped Peptide(s) | Compatibility |
|-----------|-----------|---------------|-------------------|---------------|
| hs-CRP | Elevated (>1.0 mg/L) | < 1.0 mg/L | BPC-157, KPV | High |
| HbA1c | Elevated (>5.4%) | < 5.4% | GLP-1 agonists, Semaglutide | High |
| Fasting Insulin | Elevated (>5 μIU/mL) | 2-5 μIU/mL | GLP-1, Tirzepatide | High |
| IGF-1 | Deficient (age-adjusted) | Age-stratified | Sermorelin, CJC-1295, Ipamorelin | High |
| Cortisol (AM) | Elevated (>20 μg/dL) | 10-20 μg/dL | DSIP, Epitalon | Medium |
| Cortisol (AM) | Deficient (<5 μg/dL) | 10-20 μg/dL | Sermorelin, CJC-1295 | Medium |
| TSH | Elevated (>2.5 mIU/L) | 1.0-2.0 mIU/L | Thyroid-supportive peptides | Medium |
| Free T3 | Deficient (<3.0 pg/mL) | 3.5-4.5 pg/mL | Thyroid-supportive peptides | Medium |
| Total Testosterone (male) | Deficient (<500 ng/dL) | 500-1000 ng/dL | HCG, Kisspeptin | High |
| Free Testosterone (male) | Deficient (<80 pg/mL) | 100-200 pg/mL | HCG, CJC-1295 | Medium |
| Estradiol (female) | Abnormal | Age-dependent | Kisspeptin, HCG | Medium |
| Vitamin D (25-OH) | Deficient (<40 ng/mL) | 50-70 ng/mL | General wellness support | Low |
| Vitamin B12 | Deficient (<400 pg/mL) | 500-1500 pg/mL | General wellness support | Low |
| Homocysteine | Elevated (>8 μmol/L) | < 8 μmol/L | BPC-157, GHK-Cu | Medium |
| Collagen markers | Abnormal | Varies | GHK-Cu | High |
| DHEA-S | Deficient (age-adjusted) | Age-stratified | Sermorelin, Epitalon | Medium |

The database is extensible, allowing addition of new biomarker-to-peptide mappings as clinical evidence evolves, new peptides are developed, and new biomarkers are identified through ongoing research.

---

#### COMPONENT D: AI Analysis Engine

The AI Analysis Engine processes received biomarker data through the mapping database to generate personalized peptide compatibility profiles.

**Processing Algorithm:**

1. **Input:** Normalized biomarker data set (from Component A);
2. **Loop:** For each biomarker in the input set:
   a. Query the mapping database for all records matching this biomarker;
   b. Compare the patient's value against optimal ranges and deviation thresholds;
   c. If deviation detected:
      - Retrieve mapped peptide candidate(s);
      - Assign compatibility classification (High/Medium/Low);
      - Retrieve clinical reasoning text;
      - Calculate confidence score;
   d. If no deviation detected, skip;
3. **Aggregation:** Compile all detected deviations and their peptide matches into a unified compatibility profile;
4. **Cross-Peptide Analysis:** Where multiple biomarkers point to the same peptide (e.g., both elevated hs-CRP and elevated homocysteine point to BPC-157), increase the compatibility classification and confidence score;
5. **Contraindication Check:** Flag any peptide that is contraindicated based on other biomarker values or known patient conditions;
6. **Priority Ranking:** Rank recommended peptides by aggregate compatibility score, confidence level, and therapeutic priority;
7. **Output:** Structured peptide compatibility profile ready for report generation.

**AI Enhancement Layer:**

In addition to the deterministic mapping database, the system may incorporate a machine learning model that:
- Learns from outcome data (which peptide recommendations led to biomarker improvement in subsequent tests);
- Adjusts compatibility classifications based on population-level outcome patterns;
- Identifies novel biomarker-to-peptide correlations not yet in the deterministic database;
- Personalizes recommendations based on patient demographics, genetics, and historical response patterns.

The machine learning component is optional and supplementary. The deterministic mapping database operates independently and does not require machine learning to function.

---

#### COMPONENT E: Report Generation Module

The Report Generation Module transforms the compatibility profile into a structured, human-readable report.

**Report Sections:**

1. **Patient Summary:** Overview of biomarker analysis findings, number of deviations detected, number of compatible peptides identified;
2. **Biomarker Findings:** For each biomarker analyzed: value, optimal range, deviation direction, clinical significance;
3. **Peptide Compatibility Profile:** For each recommended peptide:
   - Peptide name and category (weight loss, recovery, anti-aging, gut health, etc.);
   - Compatibility classification (High/Medium/Low);
   - Clinical reasoning (why this peptide for this patient's biomarkers);
   - Confidence score;
   - Evidence basis summary;
4. **Telemedicine Consultation Recommendation:** "Based on your biomarker profile, a telemedicine consultation is recommended to discuss peptide therapy options. Your PepPrint report will be shared with the consulting provider.";
5. **Re-Test Recommendation:** "We recommend re-testing your blood markers in 90 days to measure the effectiveness of your peptide protocol.";

**Report Formats:**
- Interactive web dashboard (patient portal);
- PDF document (downloadable, printable);
- Provider-formatted clinical report (for telemedicine consultation);
- Structured JSON payload (for API integration with EHR/telemedicine platforms);

---

#### COMPONENT F: Longitudinal Tracking Module

The Longitudinal Tracking Module stores sequential biomarker data sets and generates before-and-after comparison analyses.

**Functionality:**

1. **Baseline Storage:** The system stores the initial biomarker data set as the pre-treatment baseline;
2. **Follow-Up Comparison:** When a subsequent blood panel is processed (e.g., 90 days post-treatment), the system:
   a. Retrieves the baseline data;
   b. Calculates delta (change) for each biomarker;
   c. Determines direction of change (improved, worsened, unchanged);
   d. Calculates percentage change from baseline;
   e. Assesses whether changes are clinically significant;
3. **Therapeutic Effectiveness Score:** An aggregate score (0-100) reflecting overall biomarker improvement across the peptide protocol;
4. **Visual Timeline:** A chronological display showing biomarker values at each test point, with color-coded indicators (green = improved, yellow = unchanged, red = worsened);
5. **Protocol Adjustment Recommendations:** If certain biomarkers have not improved or have worsened, the system recommends protocol adjustments (dosage review, additional peptides, alternative therapies).

---

#### COMPONENT G: Provider Portal (PepPrint Pro)

The Provider Portal enables healthcare providers to interact with the PepPrint system in a clinical context.

**Features:**

1. **Provider Account Management:** Secure registration, credentialing verification, and subscription management;
2. **Patient Dashboard:** List of patients with their PepPrint reports, biomarker history, and current peptide protocols;
3. **Compatibility Report Viewer:** Full access to patient compatibility reports with clinical references and evidence basis;
4. **Biomarker-to-Peptide Reference:** Searchable access to the complete mapping database with clinical literature references;
5. **Telemedicine Integration:** Direct integration with telemedicine platforms for scheduling, conducting, and documenting consultations;
6. **Prescription Support:** Template-based prescription generation for recommended peptides, with dosage adjustment tools;
7. **Caseload Management:** Patient roster, appointment scheduling, follow-up reminders, protocol tracking;
8. **Outcome Analytics:** Aggregate outcome data across the provider's patient panel, showing average biomarker improvement rates by peptide type;

---

### CLAIMS

**Claim 1 (Broad Independent System Claim):**
A system for artificial intelligence-driven analysis of blood biomarker data for therapeutic peptide compatibility assessment, comprising:
(a) a biomarker data intake module configured to receive blood panel biomarker data from at least one laboratory source, said intake module supporting a plurality of input methods selected from the group consisting of: laboratory API webhooks, document upload with optical character recognition, manual data entry, and structured file import;
(b) a dual-mode data handling architecture configured to operate in:
   - a first mode wherein said biomarker data is received with associated patient identifiers as Protected Health Information in compliance with HIPAA regulations; and
   - a second mode wherein said biomarker data is received without associated patient identifiers, having been de-identified according to HIPAA Safe Harbor method prior to receipt;
   wherein said system may operate in said first mode, said second mode, or both modes simultaneously;
(c) a biomarker-to-peptide mapping database containing structured associations between blood biomarkers and therapeutic peptide candidates, said associations including biomarker deviation thresholds, peptide compatibility classifications, and clinical reasoning;
(d) an artificial intelligence analysis engine configured to process said received biomarker data through said mapping database, thereby generating a personalized peptide compatibility profile specific to the received biomarker data;
(e) a report generation module configured to transform said compatibility profile into a structured peptide compatibility report; and
(f) a processor configured to execute said intake module, said dual-mode data handling architecture, said mapping database, said analysis engine, and said report generation module.

**Claim 2 (Identified Data Mode):**
The system of Claim 1, operating in said first mode, wherein said system receives Protected Health Information including patient identifiers and maintains compliance with HIPAA regulations including encryption of data at rest using AES-256 or stronger encryption, encryption of data in transit using TLS 1.3 or stronger, role-based access controls with unique user authentication, comprehensive audit logging of all access to protected health information, automatic session logoff, and documented incident response procedures.

**Claim 3 (De-Identified Data Mode):**
The system of Claim 1, operating in said second mode, wherein said system receives biomarker data that has been de-identified by a laboratory source prior to transmission, said de-identified data comprising biomarker values and an anonymous patient token without any of the 18 identifiers specified under HIPAA Safe Harbor method (45 CFR §164.514(b)).

**Claim 4 (Biomarker-to-Peptide Mapping):**
The system of Claim 1, wherein said biomarker-to-peptide mapping database comprises mappings selected from the group consisting of:
- elevated high-sensitivity C-reactive protein mapped to BPC-157 or KPV;
- elevated HbA1c or fasting insulin mapped to GLP-1 agonists, semaglutide, or tirzepatide;
- deficient IGF-1 mapped to sermorelin, CJC-1295, or ipamorelin;
- abnormal cortisol mapped to DSIP or epitalon;
- abnormal thyroid panel mapped to thyroid-supportive peptides;
- deficient testosterone mapped to HCG or kisspeptin;
- collagen marker abnormalities mapped to GHK-Cu;
and wherein each mapping includes an optimal range distinct from standard population normal ranges, a compatibility classification, and a confidence score based on available clinical evidence.

**Claim 5 (Optimal Ranges):**
The system of Claim 4, wherein said biomarker-to-peptide mapping database utilizes optimal biomarker ranges derived from functional medicine and longevity research, said optimal ranges being narrower than standard clinical normal ranges, thereby identifying sub-clinical deviations that may benefit from therapeutic peptide intervention before reaching pathological thresholds.

**Claim 6 (Cross-Peptide Analysis):**
The system of Claim 1, wherein said artificial intelligence analysis engine further comprises a cross-peptide analysis module configured to identify instances where multiple biomarker deviations indicate the same therapeutic peptide candidate, and to increase the compatibility classification and confidence score for said peptide candidate accordingly.

**Claim 7 (Machine Learning Enhancement):**
The system of Claim 1, further comprising a machine learning model configured to:
- receive outcome data from longitudinal biomarker tracking indicating which peptide recommendations correlated with subsequent biomarker improvement;
- adjust future compatibility classifications based on population-level outcome patterns; and
- identify novel biomarker-to-peptide correlations not present in the deterministic mapping database;
wherein said machine learning model is supplementary to and does not replace the deterministic mapping database.

**Claim 8 (Longitudinal Tracking):**
The system of Claim 1, further comprising a longitudinal tracking module configured to:
- store an initial biomarker data set as a pre-treatment baseline;
- receive one or more subsequent biomarker data sets obtained after initiation of a therapeutic peptide protocol;
- calculate changes between said baseline and said subsequent data sets for each biomarker; and
- generate a therapeutic effectiveness assessment based on said calculated changes.

**Claim 9 (Provider Portal):**
The system of Claim 1, further comprising a provider portal accessible by healthcare providers, said portal providing:
- viewing access to patient peptide compatibility reports;
- access to said biomarker-to-peptide mapping database with clinical literature references;
- integration with telemedicine consultation platforms; and
- patient caseload management tools.

**Claim 10 (Telemedicine Integration):**
The system of Claim 9, further comprising a telemedicine integration layer configured to facilitate referral from said peptide compatibility report to a telemedicine consultation, enabling a healthcare provider to review said compatibility report prior to or during said consultation, and to prescribe therapeutic peptides based on said compatibility profile.

**Claim 11 (Method Claim):**
A computer-implemented method for generating personalized peptide compatibility reports from blood biomarker data, comprising the steps of:
(a) receiving blood panel biomarker data from a laboratory source, said data received in either identified form with patient identifiers or de-identified form without patient identifiers;
(b) normalizing said biomarker data to standardized units and canonical biomarker identifiers;
(c) querying a biomarker-to-peptide mapping database with said normalized biomarker data to identify biomarker deviations and associated therapeutic peptide candidates;
(d) generating a personalized peptide compatibility profile based on said query results;
(e) transforming said compatibility profile into a structured report; and
(f) delivering said report to at least one of: a patient, a healthcare provider, and a telemedicine platform.

**Claim 12 (Revenue Model):**
The system of Claim 1, further comprising a billing module configured to process payments for peptide compatibility report generation, said billing module supporting at least one of: per-report payment, monthly subscription, and revenue sharing with laboratory partners.

**Claim 13 (Extensible Database):**
The system of Claim 4, wherein said biomarker-to-peptide mapping database is extensible, allowing addition of new biomarker-to-peptide mappings as clinical evidence evolves, new therapeutic peptides are developed, and new biomarkers are identified through ongoing research.

---

### FUTURE EXTENSIONS

The applicants reserve the right to pursue continuation, divisional, or continuation-in-part applications covering:

1. **Genomic Data Integration:** Extension of the biomarker-to-peptide mapping database to include pharmacogenomic data, wherein genetic variants inform peptide selection and dosing;

2. **Microbiome Data Integration:** Extension to incorporate microbiome analysis data as an input biomarker source for peptide therapy compatibility assessment;

3. **Wearable Device Data Integration:** Incorporation of continuous health monitoring data from wearable devices (continuous glucose monitors, heart rate variability monitors, sleep trackers) as supplementary biomarker inputs;

4. **Blockchain Anchoring:** Cryptographic anchoring of biomarker data and compatibility reports to a distributed ledger, enabling immutable health record tracking and patient-owned data management (covered in related application for BioVault);

5. **Multi-Therapy Expansion:** Extension of the mapping database beyond peptides to include recommendations for supplements, nutraceuticals, pharmaceuticals, and lifestyle interventions based on biomarker profiles;

6. **Population Health Analytics:** Aggregated, de-identified analytics providing population-level insights into biomarker trends, peptide protocol effectiveness, and therapeutic outcome patterns;

7. **AI Model Expansion:** The AI analysis engine may incorporate any AI or machine learning model whether now known or hereafter developed, including but not limited to large language models, transformer architectures, graph neural networks, and reinforcement learning systems.

---

### RESERVATION OF RIGHTS

The inventor reserves all rights, including the right to file continuation, divisional, continuation-in-part, reissue, and substitute applications, and to claim the benefit of any applicable patents or applications, domestic or foreign. The scope of the present invention is not limited to the specific embodiments described herein, but encompasses all equivalents, modifications, and improvements that would be apparent to one skilled in the art.

The use of "including," "comprising," "containing," or "having" in the specification and claims is intended to be open-ended, meaning that additional elements or steps not recited may be included.

Nothing in this application shall be construed as a disclaimer of any subject matter, and the inventor reserves the right to pursue claims covering any aspect of the invention described or suggested herein.

---

*Inventor: George Mundin, Richmond, Virginia*
*Micro-Entity Status*
*Date: June 2026*
