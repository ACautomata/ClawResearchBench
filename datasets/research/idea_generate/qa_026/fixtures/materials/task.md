研究主题：EEG-based emotion recognition with deep learning。
一篇硕士论文的前两章（只有 intro + related work），声称使用 32 通道 EEG 和 LSTM 在 DEAP 数据集上达到 87% valence classification accuracy。缺信息：没有说明训练/测试 split 策略（subject-independent 还是 subject-dependent？后者会导致 inflated accuracy 因为同一 subject 的 EEG 高度相关）；没有报告 subject-wise standard deviation；没有与 DEAP benchmark 上的 published SOTA（典型为 60-70% subject-independent）对齐比较。
用户要求：生成 idea cards 但标注证据不足。
