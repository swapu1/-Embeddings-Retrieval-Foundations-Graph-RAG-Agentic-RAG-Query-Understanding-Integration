# Day 4 — Hybrid Retrieval (BM25 + Dense via Reciprocal Rank Fusion)

## Goal

Days 2 and 3 each produced a working, independently-tested retrieval method:

- **BM25** (Day 2) — keyword/term-overlap search, fast, no understanding of
  meaning.
- **PubMedBERT dense search** (Day 3) — semantic search served from a
  persisted MongoDB Atlas vector index, understands clinical shorthand and
  paraphrasing.

Day 4's job was to combine them into a single **hybrid retriever**, on the
assumption that merging two different signals should retrieve better than
either one alone — catching BM25's exact-term precision *and* PubMedBERT's
semantic recall in one pipeline.

The merging method used was **Reciprocal Rank Fusion (RRF)**.

---

## How RRF works

For a given query, run both retrievers independently. Each returns its own
ranked list of documents. RRF then assigns every document a fused score:

```
score(doc) = sum over each ranked list it appears in of:  1 / (k + rank)
```

where `rank` is the document's position in that list (1-based), and `k` is a
constant (60 is the standard default, used here). Documents are then
re-sorted by this fused score to produce the final hybrid ranking.

**Intuition:** a document ranked highly in either list contributes a large
value to its score (since `rank` is small, `1/(k+rank)` is larger). A
document ranked poorly contributes very little. A document that ranks well
in *both* lists accumulates the most — that's the mechanism intended to
reward genuine agreement between two different retrieval signals.

Critically: RRF has **no concept of which retriever is more trustworthy**.
It treats every ranked list as an equally valid vote.

---

## Setup note: a debugging detour

Before results could be produced, connecting to MongoDB Atlas from Python hit
a persistent `SSL: TLSV1_ALERT_INTERNAL_ERROR` during the TLS handshake. Over
the course of debugging, the following were tested and ruled out, in order:

1. Upgrading `certifi` and pinning `tlsCAFile` — no change.
2. Switching Python versions (3.14 → 3.12 via a fresh venv) — no change,
   ruled out Python-version incompatibility with pymongo's SSL stack.
3. Upgrading `pymongo` to the latest release (4.17.0) — no change.
4. Adding `server_api=ServerApi('1')` (MongoDB's Stable API mode) — no
   change.
5. Testing raw TCP connectivity to the Atlas host on port 27017 directly
   (bypassing pymongo entirely) — **succeeded**, which ruled out simple
   port-blocking and pointed toward something specific to the TLS layer.
6. Switching networks entirely (mobile hotspot → home wifi) — no change,
   ruling out ISP/carrier-level interference.

**Actual root cause:** a stale IP address in Atlas's Network Access
whitelist, left over from before switching networks. The current machine's
public IP no longer matched the allowed entry. Re-adding the current IP (or
temporarily allowing `0.0.0.0/0`) resolved the connection immediately.

**Lesson for future setup:** if a previously-working MongoDB Atlas
connection suddenly fails after a network change, check **Network
Access → IP whitelist** first — it's a much more common cause than driver
or TLS incompatibility, even though the error message gives no direct
indication of this.

---

## Results

Same 10-query eval set used on Days 1–3, evaluated for MRR and Hit@5.

| Method | MRR | Hit@5 |
|---|---|---|
| BM25 alone (Day 2) | 0.667 | 0.800 |
| PubMedBERT alone (Day 3) | 0.933 | 1.000 |
| **Hybrid (BM25 + PubMedBERT, RRF)** | **0.746** | **0.800** |

Hybrid retrieval performed **worse** than PubMedBERT alone on every metric —
the opposite of what combining two methods is supposed to achieve.

### Where it broke down

Two queries account for the entire drop:

| Query | PubMedBERT alone | BM25 alone | Hybrid (RRF) |
|---|---|---|---|
| "irregular heartbeat, fast rate, dizziness" | #1 | #23 | **#16** |
| "fluid overload, leg swelling, heart failure" | #1 | #22 | **#15** |

These are the same two queries that exposed BM25's core weakness back on
Day 2 — the correct documents used clinical shorthand ("AFib," "RVR,"
"CHF," "JVD," "LE edema") with essentially zero literal word overlap with
the plain-English queries. BM25 had almost nothing to score them on and
buried them near the bottom of a 26-document corpus.

PubMedBERT, working from meaning rather than literal words, ranked both of
these correctly at #1 on its own. But once fused with BM25's near-bottom
ranking for the same documents, the combined RRF score for those documents
dropped enough that other, less-relevant documents (which BM25 and
PubMedBERT both ranked moderately across the board) overtook them in the
final hybrid ranking.

---

## Why this happened — the underlying issue with naive RRF

RRF's fusion formula assumes both input rankings are **roughly equally
reliable**. In that scenario, agreement between them is a meaningful signal
and disagreement averages out harmlessly.

That assumption doesn't hold here. PubMedBERT is clearly the stronger
retriever for this corpus and query style — it correctly rejects almost
nothing and never catastrophically fails within the eval set. BM25, by
contrast, fails hard whenever the query and the document don't share
literal vocabulary, which happens more often in real clinical text (where
notes use dense shorthand) than in formal guideline-style writing.

When one retriever is meaningfully more trustworthy than the other, but RRF
gives them equal voting weight, a confidently wrong signal from the weaker
retriever can still meaningfully drag down a document the stronger
retriever got right. This is exactly what happened on both failing queries.

This is not a flaw in the implementation — it's a documented, known
limitation of unweighted RRF, and a legitimate finding rather than a bug to
fix silently.

---

## Implications going forward

1. **Hybrid retrieval is not automatically an improvement.** It needs either:
   - **Weighted fusion**, giving the stronger retriever (PubMedBERT here) more
     influence in the combined score than the weaker one (BM25), or
   - **A correction stage downstream** that can override a bad fusion
     outcome by actually reading the query and candidate document together,
     rather than trusting two independently-computed rankings blindly.

2. **This directly motivates Day 5.** Cross-encoder re-ranking takes the
   fused top-k candidates and re-scores them using a model that jointly
   encodes the query and each document — it isn't limited to combining two
   pre-computed rankings, so it has the information needed to recognize
   that "irregular heartbeat, fast rate, dizziness" and "AFib w/ RVR" are
   describing the same clinical picture, even after hybrid fusion buried
   that document.

3. **For the eval set specifically:** the fact that only 2 of 10 queries
   drove the entire performance drop is also a reminder that this synthetic
   eval set is small and not fully representative — a larger, more
   varied query set would give a more reliable picture of how often this
   failure mode actually occurs in practice.

---

## One-line summary for the weekly review

> Naive equal-weight RRF hybrid retrieval underperformed PubMedBERT alone
> (MRR 0.746 vs 0.933) because it gave BM25's confidently wrong rankings on
> shorthand-heavy queries equal weight to PubMedBERT's correct ones — a
> known limitation of unweighted rank fusion when one retriever is
> meaningfully stronger than the other. This motivates re-ranking (Day 5)
> as a correction step rather than treating hybrid fusion as a final
> answer.
