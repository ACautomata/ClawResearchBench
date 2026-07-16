研究谱系：graph attention mechanisms。
[2018] GAT — 首个将 attention 引入 GNN。Cora/CiteSeer/PubMed 上超越 GCN 1-3%。
[2019] GATv2 — 修复静态 attention 问题，改用动态 attention。
[2020] SuperGAT — 用 self-supervised edge prediction 增强 attention 学习。
[2021] Graph Transformer (GT) — 加入 positional encoding、edge features，使 GNN attention 接近 standard Transformer。
[2022] NodeFormer — kernelized attention 将 O(N^2) 降到 O(N)。
[2023] SGFormer — 单层 attention propagation 质疑'deep attention for graphs'的必要性。
当前 uncovered gaps: (1) heterophilic graphs 上 attention 的 benefit 不明确；(2) attention 可解释性在 GNN 中从未被严格验证；(3) 动态图上的 attention 几乎未被探索。
