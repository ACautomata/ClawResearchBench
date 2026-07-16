研究主题：knowledge distillation for object detection。
论文材料：传统 KD 用 KL 散度对齐 teacher-student logits，但对 detection head 不适用——分类和回归分支需要不同蒸馏策略。已有方法将 classification KD 和 localization KD 分开设计，但两个损失的权重需手工调参。
代码约束：已有 Faster R-CNN teacher（ResNet101）和 student（MobileNetV3），只能改蒸馏损失函数和权重调度，不能改 backbone 和 head 结构。
指标：mAP@0.5:0.95、KD gain（student+KD vs student 的提升量）。
