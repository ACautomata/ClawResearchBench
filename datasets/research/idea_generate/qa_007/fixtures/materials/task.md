研究主题：few-shot text classification 方法迁移。
源域方法：prompt-based few-shot classification 在情感分析（SST-2, IMDB）上表现优异，使用 GPT-style API，只需 5-shot exemplar selection + prompt template engineering。
目标域：医疗文本分类——从临床笔记中识别罕见病提及。特征：文本更长（500+ tokens）、标签高度不均衡（罕见病 <<1%）、领域术语密集。
迁移约束：不能 fine-tune 大模型，仅 API 访问，调用预算 1000 次。
