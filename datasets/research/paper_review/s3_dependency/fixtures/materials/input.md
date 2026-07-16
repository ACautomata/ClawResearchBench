请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/react-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要
ReAct 的实验依赖：
- Wikipedia API (search/lookup/finish)
- HotpotQA 23% 失败来自搜索返回空/无效信息
- ALFWorld 依赖 text-based environment interface
- WebShop 依赖 1.18M 商品的固定环境

如果 Wikipedia API 覆盖度不同，或者换成 Bing/Google 搜索，性能会怎么变？论文未做此类消融。

## 上游 Wiki 摘要
ReAct 的 thought→action→observation 循环中，observation 来自外部 API 返回。如果 API 不可用，ReAct 的 acting 环节完全失效。
