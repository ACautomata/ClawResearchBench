研究主题：text style transfer 方法迁移到 code refactoring。
源域方法：Styleformer 使用 Transformer + adversarial style classifier，将非正式文本转正式（如 gonna→going to），在 GYAFC 数据集上 BLEU=38.5 + style accuracy=92%。关键组件：(1) style classifier 提供对抗信号；(2) content preservation loss 保证语义不变。
目标域：自动 code refactoring（如 for-loop → list comprehension，mutable → immutable）。特征：(1) 代码的'语义'是执行的输入输出行为——content preservation 变成了 functional equivalence（需测试验证，而非 BLEU）；(2) 代码的'风格'有精确的 AST 约束——for→list comprehension 必须保证相同作用域和异常语义；(3) 对抗训练需要可微分编译器（不存在）。
迁移约束：不能引入可微分编译器，只能用 Python AST + test cases 做约束。
