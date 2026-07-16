研究主题：on-device keyword spotting (KWS)。
硬约束：部署在 MCU（ARM Cortex-M4, 256KB SRAM, 1MB Flash），模型必须 <200KB（int8 量化后），推理延迟 <10ms，功耗 <5mW。
已有 baseline：传统 MFCC + DNN classifier（80KB, F1=0.85 on Google Speech Commands v2 10-class 子集）。
已知问题：SOTA KWS 模型（如 BC-ResNet、TC-ResNet）F1 可达 0.94，但 <200KB 约束下量化后精度衰减严重（从 0.94 降到 0.88）。
用户偏好：TFLite Micro 兼容、PyTorch 训练 OK、不接受 cloud offloading。
