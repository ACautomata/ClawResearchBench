请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/edgereg-gnn-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游 Wiki 摘要
EdgeReg-GNN: 边感知正则化 GNN 训练方法。Cora/CiteSeer 上 1-3% 提升。论文声称代码在 github.com/example/edge-reg 但该链接访问返回 404。

## 上游问题分析摘要
P1: 正则化项具体形式未公开，无法做消融 → 调整为验证'正则化假设是否优于简单 L2'

## 上游验证设计摘要
E1: 自行实现 EdgeReg 核心逻辑 → 对比 L2 正则化 → 测是否确实有增益
