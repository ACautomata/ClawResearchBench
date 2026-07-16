研究主题：对比学习中的 batch size——挑战'larger batch = better representations'的默认假设。
默认假设：更大的 batch size 提供更多负样本，从而学到更好的表征。SimCLR 在 batch=8192 时 ImageNet linear eval 达到 70.0%，batch=256 时仅 62.4%。
反例证据：(1) MoCo v3 发现当 batch 从 4096 提升到 6144 时，ViT 的 training 变得不稳定，出现 spike——不是因为 memory，而是大 batch 下梯度统计性质改变；(2) BYOL 完全不需要负样本（batch=4096 时 74.3% vs SimCLR batch=8192 时 70.0%），说明'负样本数量 = 表征质量'的假设可能从根本上错误；(3) 在 long-tailed 数据（iNaturalist 2018）上，大 batch 对比学习导致 tail class 的表征 collapse 到少数方向——即大 batch 在类别不均衡时放大 bias。
约束：只能在 ImageNet-100 / iNaturalist 2018 子集上验证，batch size 受 8×A100 80GB 限制。
