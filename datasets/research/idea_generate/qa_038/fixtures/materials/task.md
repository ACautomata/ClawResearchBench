研究主题：低资源语言的 NLP——挑战'more data always helps'的默认假设。
默认假设：更多训练数据（即使是 noisy/synthetic）总是提升低资源语言模型性能。
反例证据：(1) 在 Quechua→Spanish 机器翻译中，加入 50K 从西班牙语反向翻译的 synthetic parallel data 后，BLEU 反而从 18.2 降到 16.7——synthetic data 将西班牙语的词序偏好强加于 Quechua (SOV vs SVO 差异)；(2) 在 Swahili NER 中，用 GPT-4 生成的标注数据替代 20% 人工标注后，F1 下降 4.3 点——LLM 的标注偏好偏向 high-resource language patterns。
约束：只能做公开低资源语言 benchmark（FLORES-200/UD 2.13/MasakhaNER），不能收集新人工标注。
