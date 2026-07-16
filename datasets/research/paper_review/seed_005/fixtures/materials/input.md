以下为claude-code任务所需的三份上游材料摘要（均从FedAux论文分析流程产出）：

## Wiki摘要
FedAux：联邦图学习可微辅助投影，三步流水线（APV→核聚合→个性化聚合），PyTorch实现

## 问题分析摘要
优先验证：P1(APV替换式消融)、P2(ogbn-arxiv异常增益诊断)、P3(Amazon方差根因)

## 验证实验设计摘要
E1: 替换式消融——将APV替换为PCA/随机投影/恒等映射/无投影4种配置，Cora 20 clients
E2: 图结构诊断——ogbn-arxiv上构造不同密度/同配性子图，对比FedAux与FedAvg增益变化
E3: 方差分解——Amazon Photo 30 seeds，分解数据划分方差/初始化方差/训练方差

注意：论文代码仓库路径未提供。论文声称代码开源但不确定是否完整可用。
