请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/adalora-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游验证设计摘要
AdaLoRA 验证实验 E1: SVD vs Adaptive 贡献分离。

AdaLoRA 仓库结构 (github.com/QingruZhang/AdaLoRA)：
- NLU/run_glue.py (训练入口，--lora_type 参数控制 PEFT 模式)
- loralib/loralib/adalora.py (AdaLoRA 核心实现，SVDLinear class 第 227-640 行，RankAllocator class)
- loralib/loralib/layers.py (LoRA 基线实现)
- NLU/scripts/ (实验脚本目录)
- NLU/data/ (GLUE 数据)
- 总计约 150 个 .py 文件
