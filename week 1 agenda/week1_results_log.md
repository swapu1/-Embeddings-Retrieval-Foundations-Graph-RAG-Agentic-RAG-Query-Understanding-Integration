# Week 1 — Retrieval Experiments Log

Running notes + numbers, updated daily. Corpus: 26-doc synthetic clinical notes
(`sample_medical_corpus.py`), 10-query eval set with 1 labeled correct doc per query.

---

## Day 1 — Embedding Model Selection

**Question:** General-purpose vs. medical-specific embedding model — does domain
pretraining actually matter for clinical text?

**Test 1 — bare abbreviation pairs (e.g. "MI" vs "myocardial infarction"):**
- MiniLM (general): 0.092 similarity
- PubMedBERT (medical): 0.928 similarity
- Caveat found: hard-negative pairs (e.g. "MI" vs "Michigan") also scored high on
  PubMedBERT (0.94) — bare short inputs are unreliable (anisotropy). Moved to
  sentence-level testing.

**Test 2 — full sentence pairs (shorthand vs. full-form, same meaning):**
- MiniLM avg: ~0.40 synonym / ~0.14 negative
- PubMedBERT avg: ~0.94 synonym / ~0.82 negative
- Relative separation still favors PubMedBERT; absolute negative scores stay high
  (expected anisotropy behavior, not a bug).

**Test 3 — full ranking test (query vs. all 26 docs, MRR / Hit@5):**

| Model | MRR | Hit@5 |
|---|---|---|
| MiniLM (general) | 0.908 | 0.900 |
| PubMedBERT (medical) | 0.933 | 1.000 |

Key finding: only 1/10 queries was genuinely synonym-dependent ("shortness of
breath and history of blood clot" → doc 0, shorthand-only). MiniLM ranked it #13
(buried). PubMedBERT ranked it #3 (visible). Other 9 queries had literal word
overlap and both models hit #1 — eval set is currently too easy; most queries
don't stress-test the model difference.

**Decision: PubMedBERT selected for Week 1 pipeline.**

**Limitation flagged:** eval set needs more paraphrase-heavy queries, and some
queries may have multiple valid correct docs (e.g. doc 0 and doc 10 both relevant
to the DVT/PE query) — current single-answer scoring doesn't account for that.

---

## Day 2 — BM25 Keyword Baseline

**Question:** How does pure keyword search compare to semantic search on the same
eval set?

| Model | MRR | Hit@5 |
|---|---|---|
| BM25 (keyword) | 0.667 | 0.800 |
| MiniLM (general semantic) | 0.908 | 0.900 |
| PubMedBERT (medical semantic) | 0.933 | 1.000 |

**Where BM25 wins:** queries with literal word overlap (e.g. "appendix
inflammation," "gallbladder inflammation") — ranked #1, same as embedding models,
essentially free wins for keyword matching.

**Where BM25 fails badly:**
- "irregular heartbeat, fast rate, dizziness" → correct doc (AFib note) ranked
  **#23**. Doc uses "AFib," "RVR" — zero literal overlap with query wording.
- "fluid overload, leg swelling, heart failure" → correct doc (CHF note) ranked
  **#22**. Doc uses "CHF exacerbation," "BNP," "JVD," "LE edema" — again zero
  literal overlap.

Both failures were ranked #1 by both embedding models on the same queries —
clean, direct evidence for why semantic search catches what keyword search
misses.

**Takeaway for Day 4 (hybrid):** BM25 and semantic search fail in different,
mostly non-overlapping places. BM25 needs literal word match or it collapses;
semantic search doesn't need literal overlap but is more compute-heavy. Hybrid
(RRF) should combine BM25's precision on exact terms with semantic's recall on
paraphrased/abbreviated queries.

---

## Next: Day 3 — Vector DB setup (persisted PubMedBERT embeddings), Day 4 — RRF
fusion of BM25 + PubMedBERT, re-run eval_set on hybrid.
