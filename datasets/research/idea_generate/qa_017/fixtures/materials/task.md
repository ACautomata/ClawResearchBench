研究主题：adversarial attack transferability。
论文材料：MI-FGSM 通过动量迭代提高对抗样本跨模型迁移性，但在防御模型（adversarial training/randomized smoothing）上成功率骤降至 <30%。
代码约束：已有 5 个预训练分类器（ResNet50/ViT/ConvNeXt/Swin/MobileNet），只能改 attack generation pipeline（PGD/优化器/surrogate ensemble），不能改目标模型。
指标：attack success rate、transfer rate、Lp perturbation budget。
