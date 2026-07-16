研究主题：医学图像分析的迁移学习——挑战'ImageNet pretraining helps all vision tasks'的默认假设。
默认假设：在 ImageNet 上预训练的模型为所有下游视觉任务提供有用的特征，包括医学图像。
反例证据：(1) 在 CheXpert（胸部 X 光）上，随机初始化的 DenseNet-121 经过充分训练后 AUC=0.842，ImageNet 预训练版本 AUC=0.841——无差异（p=0.78）；(2) 在 MIMIC-CXR 上随机初始化 vs ImageNet pretrained 的差距仅 0.5%，但用相同的 compute budget 训练 2x epochs（随机初始化）反而超过 pretrained 版本 1.2%；(3) ImageNet 的纹理偏置（texture bias）可能在医学图像中引入虚假相关性——X 光片中的诊断信息主要在形状/边界/密度，而非纹理；(4) 对于 3D 医学图像（CT/MRI），ImageNet pretraining 只能初始化 2D slice encoder，丢失了关键的 volumetric context。
约束：只能在公开医学图像数据集（CheXpert/MIMIC-CXR/RadImageNet）上验证。
