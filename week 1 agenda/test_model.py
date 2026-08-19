from sentence_transformers import SentenceTransformer, util

models = {
    "general_MiniLM": SentenceTransformer("all-MiniLM-L6-v2"),
    "medical_PubMedBERT": SentenceTransformer("pritamdeka/S-PubMedBert-MS-MARCO"),
}

# Same meaning, different wording (shorthand vs full term)
sentence_synonym_pairs = [
    ("Pt c/o SOB, hx of DVT.", "Patient complains of shortness of breath, history of deep vein thrombosis."),
    ("EKG shows acute MI.", "Electrocardiogram shows acute myocardial infarction."),
    ("Pt has hx of HTN and T2DM.", "Patient has a history of hypertension and type 2 diabetes mellitus."),
    ("CXR shows no infiltrate.", "Chest x-ray shows no infiltrate."),
    ("Started pt on Rx for AFib.", "Started patient on prescription medication for atrial fibrillation."),
]

# Genuinely different meaning (true negatives)
sentence_negative_pairs = [
    ("Pt c/o SOB, hx of DVT.", "Patient relocated from Michigan last year for work."),
    ("EKG shows acute MI.", "Patient is a retired physical education teacher."),
    ("Pt has hx of HTN and T2DM.", "Patient works for a local oil and gas company."),
]

def run_pairs(model, pairs, label):
    print(f"\n{label}:")
    for a, b in pairs:
        emb1, emb2 = model.encode([a, b])
        sim = util.cos_sim(emb1, emb2).item()
        print(f"  {a[:40]:40s} vs {b[:45]:45s} -> {sim:.3f}")

for name, model in models.items():
    print(f"\n=== {name} ===")
    run_pairs(model, sentence_synonym_pairs, "Synonym sentences (want HIGH)")
    run_pairs(model, sentence_negative_pairs, "Negative sentences (want LOW)")