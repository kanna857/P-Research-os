"""Project-related Pydantic v2 schemas for research project management."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    """Schema for creating a new research project."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Project name",
        examples=["Brain Tumor Classification with Deep Learning"],
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Detailed project description",
        examples=["Classifying brain tumors from MRI scans using CNNs."],
    )
    research_topic: str | None = Field(
        default=None,
        max_length=300,
        description="Primary research topic or area",
        examples=["Medical Image Classification"],
    )
    keywords: list[str] | None = Field(
        default=None,
        description="Relevant keywords for the research",
        examples=[["deep learning", "brain tumor", "MRI", "classification"]],
    )
    target_journal: str | None = Field(
        default=None,
        max_length=200,
        description="Target journal for publication",
        examples=["IEEE Transactions on Medical Imaging"],
    )


class ProjectUpdate(BaseModel):
    """Schema for updating an existing research project (partial update)."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated project name",
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Updated project description",
    )
    research_topic: str | None = Field(
        default=None,
        max_length=300,
        description="Updated research topic",
    )
    keywords: list[str] | None = Field(
        default=None,
        description="Updated keywords",
    )
    target_journal: str | None = Field(
        default=None,
        max_length=200,
        description="Updated target journal",
    )
    status: str | None = Field(
        default=None,
        description="Project status",
        examples=["active", "completed", "archived"],
    )


class ProjectResponse(BaseModel):
    """Schema for project data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    description: str | None = Field(default=None, description="Project description")
    research_topic: str | None = Field(default=None, description="Research topic")
    keywords: list[str] | None = Field(default=None, description="Project keywords")
    target_journal: str | None = Field(default=None, description="Target journal")
    status: str = Field(default="active", description="Current project status")
    user_id: int = Field(..., description="Owner user ID")
    created_at: datetime = Field(..., description="Project creation timestamp")
    updated_at: datetime | None = Field(
        default=None, description="Last update timestamp"
    )


class ProjectList(BaseModel):
    """Schema for paginated project list response."""

    projects: list[ProjectResponse] = Field(
        ..., description="List of projects on this page"
    )
    total: int = Field(..., ge=0, description="Total number of projects")
    page: int = Field(..., ge=1, description="Current page number")
    per_page: int = Field(..., ge=1, description="Items per page")
