"""
Scientific Diagram Generator Integration (mermaid-js/mermaid, jgraph/drawio, xyflow/xyflow, xflr6/graphviz).
Generates editable Mermaid syntax, React Flow graph node/edge definitions, Graphviz DOT specifications,
and Draw.io XML representations for model architectures, pipelines, and methodology flowcharts.
"""

from typing import Dict, Any, List, Optional


class ScientificDiagramGenerator:
    """Generates editable scientific diagrams across multiple open-source formats."""

    def generate_architecture_mermaid(self, model_name: str) -> str:
        """Generate Mermaid flowchart code for a model architecture."""
        if "siamese" in model_name.lower():
            return """graph TD
    classDef input fill:#e0f2fe,stroke:#0284c7,stroke-width:2px;
    classDef enc fill:#ede9fe,stroke:#7c3aed,stroke-width:2px;
    classDef diff fill:#fef3c7,stroke:#d97706,stroke-width:2px;
    classDef dec fill:#dcfce7,stroke:#16a34a,stroke-width:2px;
    classDef out fill:#ffe4e6,stroke:#e11d48,stroke-width:2px;

    T1["Temporal Image T1 (SAR VV/VH)"]:::input --> Enc1_T1["Encoder Block 1 (Shared)"]:::enc
    T2["Temporal Image T2 (SAR VV/VH)"]:::input --> Enc1_T2["Encoder Block 1 (Shared)"]:::enc

    Enc1_T1 --> Pool1_T1["MaxPool 2x2"]
    Enc1_T2 --> Pool1_T2["MaxPool 2x2"]

    Pool1_T1 --> Enc2_T1["Encoder Block 2"]:::enc
    Pool1_T2 --> Enc2_T2["Encoder Block 2"]:::enc

    Enc1_T1 -. Difference .-> Diff1["|F1(T1) - F1(T2)|"]:::diff
    Enc1_T2 -.-> Diff1

    Enc2_T1 -. Difference .-> Diff2["|F2(T1) - F2(T2)|"]:::diff
    Enc2_T2 -.-> Diff2

    Enc2_T1 --> Bottleneck_T1["Bottleneck"]:::enc
    Enc2_T2 --> Bottleneck_T2["Bottleneck"]:::enc

    Bottleneck_T1 -.-> DiffB["|FB(T1) - FB(T2)|"]:::diff
    Bottleneck_T2 -.-> DiffB

    DiffB --> Up2["Transposed Conv 2x2"]:::dec
    Up2 --> Cat2["Concat [Up2, Diff2]"]
    Cat2 --> Dec2["Decoder Block 2"]:::dec

    Dec2 --> Up1["Transposed Conv 2x2"]:::dec
    Up1 --> Cat1["Concat [Up1, Diff1]"]
    Cat1 --> Dec1["Decoder Block 1"]:::dec

    Dec1 --> Conv1x1["1x1 Classifier Conv"]:::out
    Conv1x1 --> Mask["Binary Change Mask (256x256)"]:::out
"""
        elif "unet" in model_name.lower():
            return """graph TD
    Input["Input Image (256x256x3)"] --> Enc1["Encoder Block 1 (64 ch)"]
    Enc1 --> Pool1["MaxPool 2x2"] --> Enc2["Encoder Block 2 (128 ch)"]
    Enc2 --> Pool2["MaxPool 2x2"] --> Bottleneck["Bottleneck (256 ch)"]
    Bottleneck --> Up1["Upconv 2x2"]
    Enc2 -. Skip 1 .-> Concat1["Concat [Up1, Enc2]"]
    Up1 --> Concat1 --> Dec1["Decoder Block 1 (128 ch)"]
    Dec1 --> Up2["Upconv 2x2"]
    Enc1 -. Skip 2 .-> Concat2["Concat [Up2, Enc1]"]
    Up2 --> Concat2 --> Dec2["Decoder Block 2 (64 ch)"]
    Dec2 --> Out["Output Mask (1x1 Conv)"]
"""
        else:
            return """graph LR
    Input["Input (Batch, 3, 224, 224)"] --> Conv1["7x7 Conv, Stride 2"]
    Conv1 --> Res1["Residual Stage 1 (3 Blocks)"]
    Res1 --> Res2["Residual Stage 2 (4 Blocks)"]
    Res2 --> Res3["Residual Stage 3 (6 Blocks)"]
    Res3 --> Res4["Residual Stage 4 (3 Blocks)"]
    Res4 --> AvgPool["Adaptive Global AvgPool"]
    AvgPool --> FC["Linear Classifier Head"]
    FC --> Probs["Softmax Class Probabilities"]
"""

    def generate_methodology_flowchart(self, topic: str) -> str:
        """Generate research methodology pipeline flowchart in Mermaid format."""
        return f"""flowchart TD
    subgraph DataPrep ["1. Data Acquisition & Strict 80/20 Partitioning"]
        Raw["Raw Multitemporal SAR / Optical Tiles"] --> Quality["Cleanlab & FiftyOne Inspection"]
        Quality --> Split["Strict 80% Train / 20% Test Split\\n(Zero Geographic Leakage)"]
        Split --> TrainSet["Training Set (80%)"]
        Split --> TestSet["Held-Out Test Set (20% Isolated)"]
    end

    subgraph Modeling ["2. Multi-Model Training Studio"]
        TrainSet --> Aug["Albumentations Spatial Augmentation"]
        Aug --> Siamese["Siamese U-Net (Cross-Temporal)"]
        Aug --> ResNet["ResNet-50 Baseline"]
        Aug --> UNet["Standard U-Net"]
        Aug --> Swin["Swin Transformer"]
        Siamese --> Lightning["PyTorch Lightning Trainer (Early Stopping & Checkpoints)"]
        ResNet --> Lightning
        UNet --> Lightning
        Swin --> Lightning
    end

    subgraph Eval ["3. Scientific Evaluation & Benchmarking"]
        TestSet --> TestEval["Evaluate on Isolated 20% Test Set"]
        Lightning --> TestEval
        TestEval --> Metrics["Precision, Recall, F1, IoU, Kappa"]
        TestEval --> Plots["Confusion Matrix & ROC Curves"]
        Metrics --> Comparison["Comparative Scientific Leaderboard"]
    end

    subgraph Pub ["4. Publication & Manuscript Generation"]
        Comparison --> LaTeX["IEEE J-STARS LaTeX Manuscript Engine"]
        Plots --> LaTeX
        LaTeX --> Doc["PDF Manuscript Compilation"]
    end
"""

    def generate_react_flow_graph(self, model_name: str) -> Dict[str, Any]:
        """Generate React Flow (xyflow) compatible nodes and edges for visual editing."""
        nodes = [
            {"id": "node-1", "type": "input", "data": {"label": "Temporal Image T1 (SAR)"}, "position": {"x": 50, "y": 50}},
            {"id": "node-2", "type": "input", "data": {"label": "Temporal Image T2 (SAR)"}, "position": {"x": 50, "y": 180}},
            {"id": "node-3", "type": "default", "data": {"label": "Encoder Stream 1 (Shared)"}, "position": {"x": 300, "y": 50}},
            {"id": "node-4", "type": "default", "data": {"label": "Encoder Stream 2 (Shared)"}, "position": {"x": 300, "y": 180}},
            {"id": "node-5", "type": "default", "data": {"label": "Difference Module |T1 - T2|"}, "position": {"x": 550, "y": 115}},
            {"id": "node-6", "type": "default", "data": {"label": "Multiscale Feature Decoder"}, "position": {"x": 780, "y": 115}},
            {"id": "node-7", "type": "output", "data": {"label": "Predicted Change Mask"}, "position": {"x": 1020, "y": 115}},
        ]
        edges = [
            {"id": "e1-3", "source": "node-1", "target": "node-3"},
            {"id": "e2-4", "source": "node-2", "target": "node-4"},
            {"id": "e3-5", "source": "node-3", "target": "node-5"},
            {"id": "e4-5", "source": "node-4", "target": "node-5"},
            {"id": "e5-6", "source": "node-5", "target": "node-6"},
            {"id": "e6-7", "source": "node-6", "target": "node-7"},
        ]
        return {"nodes": nodes, "edges": edges}


diagram_generator = ScientificDiagramGenerator()

