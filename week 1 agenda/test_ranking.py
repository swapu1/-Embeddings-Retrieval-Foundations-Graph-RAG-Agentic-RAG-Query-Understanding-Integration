from sentence_transformers import SentenceTransformer, util
from sample_medical_corpus import sample_docs, eval_set
import numpy as np

models = {
    "general_MiniLM": SentenceTransformer("all-MiniLM-L6-v2"),
    "medical_PubMedBERT": SentenceTransformer("pritamdeka/S-PubMedBert-MS-MARCO"),
}

def evaluate_model(model, docs, eval_set, top_k=5):
    # Embed all documents once (this is what you'll do for real later too)
    doc_embeddings = model.encode(docs, convert_to_tensor=True)

    reciprocal_ranks = []
    hits = []

    for query, correct_idx in eval_set:
        query_emb = model.encode(query, convert_to_tensor=True)
        sims = util.cos_sim(query_emb, doc_embeddings)[0].cpu().numpy()

        # Rank document indices by similarity, highest first
        ranked_indices = np.argsort(sims)[::-1]

        # Find where the correct document landed
        rank_position = list(ranked_indices).index(correct_idx) + 1  # 1-based rank

        reciprocal_ranks.append(1.0 / rank_position)
        hits.append(1 if rank_position <= top_k else 0)

        print(f"  Query: {query[:50]:50s} -> correct doc ranked #{rank_position}")

    mrr = np.mean(reciprocal_ranks)
    hit_rate = np.mean(hits)
    return mrr, hit_rate

for name, model in models.items():
    print(f"\n=== {name} ===")
    mrr, hit_rate = evaluate_model(model, sample_docs, eval_set)
    print(f"\n  MRR: {mrr:.3f}")
    print(f"  Hit@5: {hit_rate:.3f}")