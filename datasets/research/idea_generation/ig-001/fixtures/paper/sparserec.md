---
title: "SparseRec: Sparse Routing For Retrieval"
authors: ["Bench Author"]
year: 2026
---
We replace the dense item tower with top-k sparse routing (k=8). On the same
MovieLens-1M split we get Recall@20 = 0.16, but inference FLOPs drop 40%.
