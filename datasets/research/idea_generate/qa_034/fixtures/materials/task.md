研究主题：图像 data augmentation 方法迁移到时序数据。
源域方法：RandAugment 在图像分类上通过随机组合 14 种基础变换（旋转/翻转/色彩等），在 CIFAR/ImageNet 上稳定提升 2-3%。关键设计：(1) 全局幅度参数 M 控制所有变换强度，(2) 每 batch 随机选择 N 种变换。
目标域：multivariate time series classification（如 UEA archive: HumanActivityRecognition, PenDigits）。特征：(1) 每个 channel 有不同的物理量纲（加速度 vs 陀螺仪），不可统一缩放；(2) 时间轴的变换（warping/pooling）会破坏因果性（不能用未来信息）；(3) channel 之间的相关性（如三轴加速度）有物理意义，不可独立扰动。
迁移约束：只能做离线训练（batch processing），推理延迟 <50ms，必须保持时间因果性。
