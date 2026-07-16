研究主题：deep GNN oversmoothing 问题。
论文 A（ResGCN）：声称带 residual connections 的深度 GNN（>8 层）彻底解决 oversmoothing，在 Cora 上 16 层仍持续增益。
论文 B（DeepGC）：在相同 Cora/CiteSeer/PubMed 上实验，发现 residual 仅延迟 oversmoothing 而非消除——超过 16 层后节点表示仍坍缩。指出论文 A 的 train/test split 泄露。
约束：只能在 Cora/CiteSeer/PubMed 上设计验证实验，代码不可用。
