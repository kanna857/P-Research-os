"""
Model Registry: Provides standard and scientific vision architectures.
Supports: ResNet, MobileNet, DenseNet, EfficientNet, Inception, U-Net, Siamese U-Net, ViT, Swin Transformer.
"""

from typing import Dict, Any, List, Optional
import torch
import torch.nn as nn


class SiameseUNet(nn.Module):
    """
    Siamese U-Net architecture for multitemporal change detection (Sentinel-1 SAR / Optical).
    Twin encoders with shared weights, differential cross-feature subtraction, and transposed conv decoder.
    """

    def __init__(self, in_channels: int = 2, num_classes: int = 2):
        super().__init__()
        # Encoder block 1
        self.enc1 = nn.Sequential(
            nn.Conv2d(in_channels, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )
        self.pool1 = nn.MaxPool2d(2)

        # Encoder block 2
        self.enc2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
        )
        self.pool2 = nn.MaxPool2d(2)

        # Bottleneck
        self.bottleneck = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
        )

        # Decoder with difference feature fusion
        self.up2 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.dec2 = nn.Sequential(
            nn.Conv2d(256, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
        )

        self.up1 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.dec1 = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )

        self.classifier = nn.Conv2d(64, num_classes, kernel_size=1)

    def forward(self, t1: torch.Tensor, t2: Optional[torch.Tensor] = None) -> torch.Tensor:
        if t2 is None:
            # If concatenated or single input, split channels
            if t1.shape[1] >= 4:
                t2 = t1[:, 2:, :, :]
                t1 = t1[:, :2, :, :]
            else:
                t2 = t1

        # Twin encoder pass
        e1_t1 = self.enc1(t1)
        e1_t2 = self.enc1(t2)
        diff_e1 = torch.abs(e1_t1 - e1_t2)

        e2_t1 = self.enc2(self.pool1(e1_t1))
        e2_t2 = self.enc2(self.pool1(e1_t2))
        diff_e2 = torch.abs(e2_t1 - e2_t2)

        b_t1 = self.bottleneck(self.pool2(e2_t1))
        b_t2 = self.bottleneck(self.pool2(e2_t2))
        diff_b = torch.abs(b_t1 - b_t2)

        # Decoder pass
        d2 = self.up2(diff_b)
        d2 = torch.cat([d2, diff_e2], dim=1)
        d2 = self.dec2(d2)

        d1 = self.up1(d2)
        d1 = torch.cat([d1, diff_e1], dim=1)
        d1 = self.dec1(d1)

        out = self.classifier(d1)
        return out


def get_available_model_families() -> List[Dict[str, Any]]:
    """Return catalog of supported model architectures."""
    return [
        {
            "id": "resnet-50",
            "name": "ResNet-50",
            "family": "ResNet",
            "parameter_count": "25.6M",
            "category": "Classification",
            "description": "Deep residual network with bottleneck architecture, robust spatial feature extractor.",
            "suitable_for": ["Baseline Feature Extraction", "Benchmark Comparison"],
        },
        {
            "id": "mobilenet-v3",
            "name": "MobileNetV3-Large",
            "family": "MobileNet",
            "parameter_count": "5.4M",
            "category": "Lightweight Classification",
            "description": "Hardware-efficient inverted bottleneck with squeeze-and-excitation attention.",
            "suitable_for": ["Edge / On-Device Deployment", "Rapid Prototyping"],
        },
        {
            "id": "densenet-121",
            "name": "DenseNet-121",
            "family": "DenseNet",
            "parameter_count": "8.0M",
            "category": "Classification",
            "description": "Densely connected convolutional layers maximizing feature reuse across depth.",
            "suitable_for": ["High-Resolution Pattern Recognition", "Medical & Geospatial"],
        },
        {
            "id": "efficientnet-b4",
            "name": "EfficientNet-B4",
            "family": "EfficientNet",
            "parameter_count": "19.3M",
            "category": "Classification",
            "description": "Compound scaling across depth, width, and resolution.",
            "suitable_for": ["Fine-grained Classification"],
        },
        {
            "id": "unet-standard",
            "name": "Standard U-Net",
            "family": "U-Net",
            "parameter_count": "31.0M",
            "category": "Segmentation",
            "description": "Symmetric encoder-decoder with skip connections for pixel-accurate mask generation.",
            "suitable_for": ["Segmentation", "Change Mask Generation"],
        },
        {
            "id": "siamese-unet",
            "name": "Siamese U-Net (Dual-Branch Cross-Temporal)",
            "family": "Siamese U-Net",
            "parameter_count": "34.2M",
            "category": "Change Detection",
            "description": "State-of-the-art dual-branch temporal feature subtraction network with multiscale skip connections.",
            "suitable_for": ["Sentinel-1 SAR Change Detection", "Multitemporal Satellite Analysis"],
        },
        {
            "id": "vision-transformer-b16",
            "name": "ViT-Base/16",
            "family": "Vision Transformer",
            "parameter_count": "86.6M",
            "category": "Transformer",
            "description": "Pure self-attention over non-overlapping 16x16 image patches.",
            "suitable_for": ["Global Context Modeling", "Large-scale Pretraining"],
        },
        {
            "id": "swin-transformer-tiny",
            "name": "Swin Transformer (Tiny)",
            "family": "Swin Transformer",
            "parameter_count": "28.3M",
            "category": "Hierarchical Transformer",
            "description": "Shifted window self-attention providing linear computational complexity with image size.",
            "suitable_for": ["Dense Prediction", "Remote Sensing Segmentation"],
        },
    ]
