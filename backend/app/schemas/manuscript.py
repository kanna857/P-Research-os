"""Manuscript-related Pydantic v2 schemas for writing, references, and export."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SectionContent(BaseModel):
    """Schema for a single manuscript section."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Section title / heading",
        examples=["Introduction"],
    )
    content: str | None = Field(
        default=None,
        description="Section body text (Markdown or LaTeX)",
    )
    order: int = Field(
        ...,
        ge=0,
        description="Display order of the section (0-indexed)",
    )


class ManuscriptCreate(BaseModel):
    """Schema for creating a new manuscript."""

    project_id: int = Field(..., description="Associated project ID")
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Manuscript title",
        examples=["Deep Learning for Brain Tumor Classification: A Comprehensive Study"],
    )
    template: str = Field(
        default="ieee",
        description="Manuscript template / style",
        examples=["ieee", "acm", "springer", "elsevier", "nature"],
    )


class ManuscriptUpdate(BaseModel):
    """Schema for updating an existing manuscript (partial update)."""

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Updated manuscript title",
    )
    abstract: str | None = Field(
        default=None,
        max_length=5000,
        description="Manuscript abstract",
    )
    keywords: list[str] | None = Field(
        default=None,
        description="Manuscript keywords",
        examples=[["deep learning", "brain tumor", "classification"]],
    )
    sections: list[SectionContent] | None = Field(
        default=None,
        description="Updated manuscript sections",
    )
    template: str | None = Field(
        default=None,
        description="Updated template / style",
    )
    status: str | None = Field(
        default=None,
        description="Manuscript status",
        examples=["draft", "review", "final", "submitted"],
    )


class ManuscriptResponse(BaseModel):
    """Schema for manuscript data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique manuscript identifier")
    project_id: int = Field(..., description="Associated project ID")
    title: str = Field(..., description="Manuscript title")
    abstract: str | None = Field(default=None, description="Manuscript abstract")
    keywords: list[str] | None = Field(default=None, description="Manuscript keywords")
    sections: list[dict] | None = Field(
        default=None, description="Manuscript sections"
    )
    template: str = Field(default="ieee", description="Template / style in use")
    references: list[dict] | None = Field(
        default=None, description="Embedded references"
    )
    status: str = Field(
        default="draft",
        description="Manuscript status",
        examples=["draft", "review", "final", "submitted"],
    )
    version: int = Field(default=1, description="Manuscript version number")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime | None = Field(
        default=None, description="Last update timestamp"
    )


class GenerateSectionRequest(BaseModel):
    """Schema for requesting AI-generated section content."""

    section_type: str = Field(
        ...,
        description="Type of section to generate",
        examples=["introduction", "methods", "results", "discussion", "conclusion"],
    )
    context: dict | None = Field(
        default=None,
        description="Contextual data for generation (project info, metrics, etc.)",
    )
    style: str | None = Field(
        default="academic",
        description="Writing style",
        examples=["academic", "concise", "detailed"],
    )


class RewriteRequest(BaseModel):
    """Schema for requesting text rewriting / paraphrasing."""

    text: str = Field(
        ...,
        min_length=1,
        description="Text to rewrite",
    )
    style: str = Field(
        default="academic",
        description="Target writing style",
        examples=["academic", "concise", "formal"],
    )
    target_journal: str | None = Field(
        default=None,
        description="Target journal for style matching",
        examples=["IEEE Transactions on Medical Imaging"],
    )


class GrammarCheckResponse(BaseModel):
    """Schema for grammar / style check results."""

    original: str = Field(..., description="Original text that was checked")
    corrected: str = Field(..., description="Corrected text")
    matches: list[dict] = Field(
        default_factory=list,
        description="Individual grammar / style issues found",
    )


class ReferenceCreate(BaseModel):
    """Schema for manually adding a reference."""

    project_id: int = Field(..., description="Associated project ID")
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Reference title",
    )
    authors: list[dict] | None = Field(
        default=None,
        description="List of authors with name fields",
        examples=[[{"given": "John", "family": "Smith"}]],
    )
    year: int | None = Field(
        default=None,
        ge=1900,
        le=2100,
        description="Publication year",
    )
    doi: str | None = Field(
        default=None,
        description="Digital Object Identifier",
        examples=["10.1109/TMI.2024.1234567"],
    )
    venue: str | None = Field(
        default=None,
        description="Journal or conference name",
    )
    bibtex: str | None = Field(
        default=None,
        description="BibTeX entry",
    )


class ReferenceResponse(BaseModel):
    """Schema for reference data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique reference identifier")
    project_id: int = Field(..., description="Associated project ID")
    title: str = Field(..., description="Reference title")
    authors: list[dict] | None = Field(default=None, description="Reference authors")
    year: int | None = Field(default=None, description="Publication year")
    doi: str | None = Field(default=None, description="DOI")
    venue: str | None = Field(default=None, description="Journal / conference")
    bibtex: str | None = Field(default=None, description="BibTeX entry")
    ris: str | None = Field(default=None, description="RIS formatted entry")
    source_paper_id: int | None = Field(
        default=None, description="Linked paper ID if auto-imported"
    )
    verified: bool = Field(
        default=False, description="Whether the reference has been verified"
    )
    created_at: datetime = Field(..., description="Record creation timestamp")


class ExportFormat(BaseModel):
    """Schema for manuscript export options."""

    format: str = Field(
        default="pdf",
        description="Export file format",
        examples=["pdf", "latex", "docx", "html"],
    )
    include_figures: bool = Field(
        default=True,
        description="Whether to include figures in the export",
    )
