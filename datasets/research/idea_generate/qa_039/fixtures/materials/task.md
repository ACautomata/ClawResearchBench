研究主题：heterophilic graphs 上的 GNN——挑战'deeper GNNs capture better representations'的默认假设。
默认假设：更深的 GNN（更多层）能捕获更长程的依赖，从而提升节点分类性能。
反例证据：(1) 在 heterophilic graph benchmark（Roman-Empire/Amazon-Ratings/Questions）上，2 层 GCN 的 accuracy 为 63.2%，加深到 8 层后反而降至 51.1%——heterophily 导致邻居信息与中心节点标签负相关，加深会放大错误信号；(2) LINKX（仅用 MLP on raw features + adjacency features）在 Questions 数据集上 2 层就达到 74.1%，超过 8 层 GCN 的 51.1% 超过 23 个点——说明 heterophilic 图上的有效信息主要在节点特征本身，而非邻居聚合。
约束：只能在公开 heterophilic benchmark（Roman-Empire/Amazon-Ratings/Questions/Chameleon）上验证。
