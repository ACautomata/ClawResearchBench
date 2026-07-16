研究主题：real-time video action recognition on consumer GPU。
硬约束：单张 GTX 1660（6GB VRAM），必须处理 30fps 视频流（即每帧 <33ms），batch size=1（在线推理），功耗无限制但不可用云端。
已有 baseline：MobileNetV3-Small + TSM（Temporal Shift Module），在 UCF-101 上 top-1=78.3%，推理 22ms/frame。
已知问题：VideoMAE/VideoSwin 等 SOTA 在 UCF-101 上 top-1=95%+，但需要 100ms+/frame，无法实时。
约束：不能在训练时用更多 GPU，但推理时可以使用 temporal batching 如果设计得当。
