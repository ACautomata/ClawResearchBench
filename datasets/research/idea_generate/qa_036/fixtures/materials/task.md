研究主题：graph pooling 方法迁移到 point cloud downsampling。
源域方法：DiffPool 在图分类中通过可微分软分配矩阵，将 N 个节点层次化聚合为 K 个 cluster（N→K 粗化），在 PROTEINS/NCI1 上提升 GNN 分类精度。关键：(1) 分配矩阵 S 由 GNN 生成，(2) 粗化后的图保留邻接结构。
目标域：3D point cloud downsampling for classification（如 ModelNet40 keypoint selection）。特征：(1) 点云没有显式邻接矩阵——需基于 k-NN/radius 动态构图；(2) 3D 空间有刚体变换不变性要求（SE(3) invariance）——graph pooling 的分配矩阵不是 SE(3)-invariant；(3) 点云密度不均匀——近处点密、远处点稀，固定 K 的粗化会偏向近处。(4) 局部几何特征（法向量/曲率）可能需要额外的编码。
迁移约束：已有 PointNet++ baseline，只能改 downsampling 策略。
