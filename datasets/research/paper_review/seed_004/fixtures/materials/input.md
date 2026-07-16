## 上游Wiki摘要
FedAux：APV可微投影→核聚合→个性化聚合。数据集：Cora/CiteSeer/PubMed/ogbn-arxiv/Amazon。Baseline：FedAvg/FedProx/SCAFFOLD等12个。

## 上游问题分析摘要（该文档位于上一阶段产出中）
优先验证问题（高优先级）：
P1: APV增益是否来自'可微投影'本身还是任何投影均有效？消融仅测试移除APV，缺乏替换式对比（PCA/随机投影/恒等映射）
P2: ogbn-arxiv上3.7%异常高增益的原因？其他5个数据集增益仅1.5-2.5%
P3: Amazon上方差增大根因？Photo上FedAux方差0.9% vs FedAvg 0.4%

低优先级：
P4: 通信轮数是否过度？200轮可能超过收敛所需
P5: client数量增大到100+时核聚合是否退化
