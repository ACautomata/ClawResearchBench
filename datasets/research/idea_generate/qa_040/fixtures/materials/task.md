研究主题：长序列处理——挑战'attention captures all dependencies'的默认假设。
默认假设：Transformer 的 self-attention 可以捕获任意距离的依赖关系，注意力图反映了 token 间的真实语义关联。
反例证据：(1) 在 Long Range Arena (LRA) benchmark 的 Pathfinder 任务（判断两点是否由路径连接）上，标准 Transformer 的 accuracy 仅 50.3%（≈随机猜测），而状态空间模型 S4 达到 92.3%——self-attention 在需要精确空间推理的长程任务上完全失败；(2) 注意力图可视化显示，在后层中大多数 token 的注意力集中在 [CLS] 和前几个 token（所谓的 attention sink），而非语义相关的 token——即注意力机制退化为固定的静态模式，失去动态选择能力。
约束：只能在 LRA benchmark 上验证，不设计新的长序列任务。
