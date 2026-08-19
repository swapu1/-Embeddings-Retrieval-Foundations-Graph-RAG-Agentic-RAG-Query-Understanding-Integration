"""
Synthetic medical corpus for learning/prototyping the Week 1 retrieval pipeline.
NOT clinically accurate — for testing embedding models, BM25, hybrid retrieval, etc.
"""

sample_docs = [
    # --- Discharge summaries (abbreviation-heavy) ---
    "Pt c/o SOB x2 days, hx of DVT 6mo ago. R/o PE. Started on heparin gtt. Plan: CTA chest, monitor sats.",
    "65yo M w/ hx HTN, T2DM presents w/ CP radiating to L arm. EKG shows ST elevation. Dx: acute MI. Sent to cath lab.",
    "Pt w/ hx COPD presents w/ worsening dyspnea, productive cough. CXR shows infiltrate. Dx: pneumonia. Started on abx.",
    "58yo F c/o palpitations, dizziness. Hx AFib. EKG confirms AFib w/ RVR. Started on dilt gtt, rate controlled.",
    "Pt admitted for CHF exacerbation, BNP elevated, JVD +, bilateral LE edema. Diuresed w/ IV lasix, improved.",

    # --- Radiology reports (templated, terse) ---
    "CT chest w/ contrast: filling defect in R main pulmonary artery c/w acute PE. No evidence of RV strain.",
    "CXR PA/lateral: no acute cardiopulmonary process. Heart size normal. No effusion or infiltrate.",
    "MRI brain w/o contrast: no acute infarct, hemorrhage, or mass. Mild age-related atrophy.",
    "US abdomen: gallbladder wall thickening, pericholecystic fluid c/w acute cholecystitis.",
    "CT abdomen/pelvis: appendix dilated to 12mm w/ surrounding fat stranding, c/w acute appendicitis.",

    # --- Clinical guidelines (formal, full terminology) ---
    "Patients presenting with acute dyspnea and a history of deep vein thrombosis should be risk-stratified using the Wells criteria for pulmonary embolism.",
    "First-line treatment for stage 2 hypertension includes thiazide diuretics or ACE inhibitors, with lifestyle modification counseling.",
    "In patients with suspected myocardial infarction, a 12-lead electrocardiogram should be obtained within 10 minutes of presentation.",
    "Antibiotic selection for community-acquired pneumonia should be guided by severity assessment using the CURB-65 score.",
    "Anticoagulation therapy in atrial fibrillation should be guided by CHA2DS2-VASc score to assess stroke risk.",

    # --- Nursing notes (informal, shorthand) ---
    "pt anxious, RR 24, spo2 91% RA, notify MD",
    "pt ambulating in hallway w/ min assist, tolerating well, no c/o pain",
    "pt refused breakfast, states nauseated, gave zofran prn per order",
    "vitals stable, afebrile, pain 3/10 at incision site, dressing dry and intact",
    "pt confused, oriented x1, family at bedside, MD aware, will monitor",

    # --- Medication / prescription notes ---
    "Rx: Metformin 500mg PO BID, Lisinopril 10mg PO daily, Atorvastatin 20mg PO qHS.",
    "Pt started on Warfarin 5mg daily, INR to be checked in 3 days, target range 2-3.",
    "D/c'd home on Amoxicillin 500mg TID x7 days for community-acquired pneumonia.",

    # --- Hard negative / ambiguous abbreviation traps ---
    "Pt relocated from Michigan last year, denies chest pain, here for routine physical exam.",
    "Pt is a retired physical education (PE) teacher, presents for annual wellness visit.",
    "Pt works for a local oil company, no occupational exposure concerns noted.",
]

# Synonym pairs for testing embedding model domain sensitivity (Day 1 diagnostic)
synonym_pairs = [
    ("MI", "myocardial infarction"),
    ("SOB", "shortness of breath"),
    ("DVT", "deep vein thrombosis"),
    ("PE", "pulmonary embolism"),
    ("hx", "history"),
    ("c/o", "complains of"),
    ("CXR", "chest x-ray"),
    ("Rx", "prescription"),
    ("HTN", "hypertension"),
    ("T2DM", "type 2 diabetes mellitus"),
    ("AFib", "atrial fibrillation"),
    ("CHF", "congestive heart failure"),
]

# Hard negatives — same abbreviation, wrong meaning (tests false-positive risk)
hard_negative_pairs = [
    ("MI", "Michigan"),
    ("PE", "physical education"),
    ("BP", "British Petroleum"),
]

# Small labeled eval set: (query, index of relevant doc in sample_docs)
eval_set = [
    ("patient with shortness of breath and history of blood clot, concern for lung clot", 0),
    ("chest pain radiating to arm, EKG changes", 1),
    ("worsening cough and shortness of breath with lung infiltrate", 2),
    ("irregular heartbeat, fast rate, dizziness", 3),
    ("fluid overload, leg swelling, heart failure", 4),
    ("CT scan showing clot in lung artery", 5),
    ("gallbladder inflammation on ultrasound", 8),
    ("appendix inflammation on CT", 9),
    ("stroke risk scoring for irregular heartbeat", 14),
    ("antibiotic choice for pneumonia severity", 13),
]

if __name__ == "__main__":
    print(f"Corpus size: {len(sample_docs)} documents")
    print(f"Synonym pairs: {len(synonym_pairs)}")
    print(f"Hard negative pairs: {len(hard_negative_pairs)}")
    print(f"Eval queries: {len(eval_set)}")
