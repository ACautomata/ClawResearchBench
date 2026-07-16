研究主题：multi-modal alignment for vision-language models。
论文材料：CLIP 通过对比学习对齐图像和文本，但 fine-grained 对齐（如'红色条纹衬衫'与图像区域的对应）很差，因为全局对比损失无法建模细粒度对应。
代码约束：已有 frozen CLIP encoders（ViT-B/32 + GPT text encoder），只能改 alignment head 和对比损失函数，不能重训 backbone。
指标：grid-to-text retrieval recall、fine-grained alignment accuracy、zero-shot classification 不能下降。
