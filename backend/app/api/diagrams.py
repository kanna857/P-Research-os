"""
Scientific diagram generator API routes (Mermaid, React Flow, Graphviz, Draw.io).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.diagram import Diagram
from app.integrations.diagrams.diagram_generator import diagram_generator

router = APIRouter()


@router.get("/templates")
async def get_diagram_templates():
    """Retrieve scientific diagram templates."""
    return [
        {
            "id": "siamese-unet-arch",
            "name": "Siamese U-Net Architecture",
            "type": "architecture",
            "code": diagram_generator.generate_architecture_mermaid("Siamese U-Net"),
        },
        {
            "id": "change-detection-methodology",
            "name": "Research Methodology Pipeline",
            "type": "flowchart",
            "code": diagram_generator.generate_methodology_flowchart("Sentinel-1 SAR Change Detection"),
        },
        {
            "id": "standard-unet-arch",
            "name": "Standard U-Net Pipeline",
            "type": "architecture",
            "code": diagram_generator.generate_architecture_mermaid("Standard U-Net"),
        },
    ]


@router.get("/project/{project_id}")
async def get_project_diagrams(project_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve saved diagrams for project."""
    result = await db.execute(select(Diagram).where(Diagram.project_id == project_id))
    return result.scalars().all()


@router.post("")
async def save_diagram(data: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    """Save an editable diagram to project."""
    diagram = Diagram(
        project_id=data.get("project_id", 1),
        name=data.get("name", "Research Methodology Diagram"),
        diagram_type=data.get("diagram_type", "mermaid"),
        content=data.get("content", diagram_generator.generate_methodology_flowchart("Change Detection")),
        format=data.get("format", "mermaid"),
    )
    db.add(diagram)
    await db.commit()
    await db.refresh(diagram)
    return diagram


@router.get("/react-flow/{model_name}")
async def get_react_flow_nodes(model_name: str):
    """Return interactive React Flow nodes and edges for visual editing."""
    return diagram_generator.generate_react_flow_graph(model_name)

