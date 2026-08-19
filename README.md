# Clinical AI Retrieval Pipeline — 3-Week Build

Internship project: building a medical document retrieval system end-to-end,
starting from basic search and progressing to agentic, multi-step retrieval.
Corpus, code, and experiment logs live in this repo.

---

## Overview

| Week | Focus | Output |
|---|---|---|
| 1 | Embeddings & Retrieval Foundations | Working hybrid + re-ranked retrieval pipeline |
| 2 | Graph RAG for Medical Use Cases | Graph-based retrieval + deployment complexity analysis |
| 3 | Agentic RAG, Query Understanding & Integration | Multi-step, self-correcting retrieval agent |

---

## Week 1 — Embeddings & Retrieval Foundations

**Goal:** establish a solid retrieval baseline before layering anything more
complex on top.

- [x] **Day 1 — Embedding model survey.** Compared general-purpose
  (MiniLM) vs. medical-domain (PubMedBERT) embeddings on clinical
  synonym/abbreviation resolution. PubMedBERT selected — MRR 0.933 vs 0.908,
  Hit@5 1.000 vs 0.900. Full writeup: `week1_results_log.md`, `Day1_Summary.pdf`.
- [x] **Day 2 — BM25 sparse baseline.** Keyword-only retrieval evaluated on the
  same query set. MRR 0.667 — strong on literal-overlap queries, collapses
  (rank #22-23) on paraphrased/abbreviated ones. Confirms need for hybrid.
- [ ] **Day 3 — Semantic retrieval via vector DB.** Persist PubMedBERT
  embeddings in a proper vector store (Chroma/Qdrant/MongoDB Atlas) instead of
  re-encoding per query. Re-run cosine similarity search through the DB layer.
- [ ] **Day 4 — Hybrid retrieval (BM25 + dense).** Combine sparse and dense
  rankings via Reciprocal Rank Fusion (RRF). Re-evaluate MRR/Hit@5 against both
  individual methods.
- [ ] **Day 5 — Re-ranking.** Add a cross-encoder re-ranking pass (local
  cross-encoder or Cohere Rerank) over hybrid top-k results. Final pipeline
  comparison table across all four methods (BM25 / dense / hybrid / re-ranked).

**Deliverables:** performance comparison table, GitHub repo structure, latency
benchmark, worked qualitative example (clinical query walked through all four
methods).

---

## Week 2 — Graph RAG for Medical Use Cases

**Goal:** understand where relationship-aware retrieval beats vector-only
retrieval, and what it costs to run in a real clinical setting.

- [ ] **Study Graph RAG architecture.** Where it helps over vector-only RAG —
  e.g. multi-hop clinical relationships (drug → interaction → contraindication →
  condition) that flat vector similarity can't easily capture.
- [ ] **Automate graph construction.** Build a pipeline that extracts entities
  and relationships from the corpus (e.g. LLM-based entity/relation extraction,
  or a medical NER model) and populates a graph store (Neo4j or similar).
- [ ] **Document deployment complexity.** Identify and write up the bottlenecks
  of running Graph RAG in a clinical setting — graph construction cost,
  maintenance/update overhead as new notes arrive, latency vs. vector-only,
  and failure modes specific to noisy/inconsistent clinical entity extraction.

**Deliverable:** working (even if small-scale) Graph RAG pipeline + a written
bottleneck/complexity analysis comparing it against Week 1's hybrid pipeline.

---

## Week 3 — Agentic RAG, Query Understanding & Integration

**Goal:** move from a static retrieval pipeline to one that reasons about the
query first and adapts its own retrieval strategy.

- [ ] **Agentic RAG patterns.** Study and implement multi-step retrieval,
  tool-calling, and self-correction — e.g. the agent decides whether a query
  needs vector search, graph traversal, or both, and can retry/re-route if the
  first retrieval pass looks insufficient.
- [ ] **Query translation / rewriting.** Build a pre-retrieval step that expands
  clinical shorthand, abbreviations, and underspecified queries into fuller,
  retrieval-ready form before they hit the pipeline (e.g. LLM-based rewriting,
  or a dedicated medical abbreviation-expansion layer). This directly targets
  the shorthand/paraphrase gap identified in Week 1, Day 2's BM25 results.

**Deliverable:** end-to-end agentic pipeline — query in, routed and rewritten
as needed, retrieved via the best-fit strategy (hybrid/graph), and returned —
plus a short demo of the query-rewriting step handling a genuinely
underspecified clinical query.

---

## Repo Structure (target, by end of Week 3)

```
clinical-ai-retrieval/
├── data/
│   └── sample_medical_corpus.py       # Week 1 synthetic corpus + eval set
├── week1_retrieval/
│   ├── 01_embedding_survey.py
│   ├── 02_bm25_baseline.py
│   ├── 03_dense_retrieval.py
│   ├── 04_hybrid_rrf.py
│   └── 05_reranking_eval.py
├── week2_graph_rag/
│   ├── graph_construction_pipeline.py
│   └── deployment_complexity_notes.md
├── week3_agentic_rag/
│   ├── agent_router.py
│   └── query_rewriting.py
├── week1_results_log.md               # running experiment log
└── README.md                          # this file
```

## Status

Currently on **Week 1, Day 3** (vector DB setup). Days 1-2 complete with
results logged in `week1_results_log.md`.
