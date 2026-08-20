# Retrieval Methods Comparison — Summary

## Results So Far

| Method | MRR | Hit@5 |
|---|---|---|
| BM25 alone (Day 2) | 0.667 | 0.800 |
| PubMedBERT alone (Day 3) | 0.933 | 1.000 |
| Hybrid RRF (Day 4) | 0.746 | 0.800 |
| Re-ranked (Day 5) | 0.839 | 0.900 |

## The Honest Read

Re-ranking recovered most of what hybrid fusion lost, but didn't fully close the gap back to PubMedBERT-alone's performance (0.839 vs 0.933 MRR). That gap is worth investigating rather than reporting as a clean win.

## Remaining Failure Case

**Query:** `patient with shortness of breath and history of bl...`
**Result:** correct doc ranked **#18**

Likely one of the two known problem queries from Day 4 (possibly a new one or a variant — worth confirming). A rank of #18 means the correct document is still buried near the bottom of the top-20 candidate pool.

## Key Takeaway

Re-ranking can only reorder what hybrid retrieval hands it — it fixes **ordering** problems, not **retrieval** (missing-from-candidates) problems. If the correct document isn't meaningfully present in the top-20 candidates to begin with (e.g., pushed down by RRF fusion, or effectively "vetoed" by one retriever), re-ranking can't rescue it.

**Conclusion for writeup:** Re-ranking is not a universal fix for hybrid retrieval's weaknesses. It only helps when the correct document is already in the candidate pool, just ranked poorly.
