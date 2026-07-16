研究主题：code generation evaluation metrics。
论文材料：CodeBERTScore 使用 BERT 嵌入计算生成代码与参考代码的语义相似度，但忽略了代码的执行正确性——语义相似但功能不同的代码仍得高分。
代码约束：已有 HumanEval + MBPP test harness（包括 test case runner），只能改 scoring function 和 test case sampling 策略，不能改模型。
指标：pass@k、functional correctness rate、与人工评分的 Spearman 相关系数。
