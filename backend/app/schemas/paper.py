"""Paper-related Pydantic v2 schemas for literature search, download, and analysis."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PaperSearch(BaseModel):
    """Schema for searching academic papers across multiple sources."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Search query string",
        examples=["brain tumor classification deep learning MRI"],
    )
    sources: list[str] | None = Field(
        default=["openalex", "semanticscholar", "crossref"],
        description="Academic sources to search",
        examples=[["openalex", "semanticscholar", "crossref"]],
    )
    year_from: int | None = Field(
        default=None,
        ge=1900,
        le=2100,
        description="Filter papers published from this year",
        examples=[2020],
    )
    year_to: int | None = Field(
        default=None,
        ge=1900,
        le=2100,
        description="Filter papers published up to this year",
        examples=[2024],
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of results to return",
    )
    open_access_only: bool = Field(
        default=False,
        description="Return only open-access papers",
    )


class PaperResponse(BaseModel):
    """Schema for paper data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique paper identifier")
    project_id: int = Field(..., description="Associated project ID")
    title: str = Field(..., description="Paper title")
    authors: list[str] | None = Field(default=None, description="List of author names")
    abstract: str | None = Field(default=None, description="Paper abstract")
    doi: str | None = Field(default=None, description="Digital Object Identifier")
    year: int | None = Field(default=None, description="Publication year")
    venue: str | None = Field(
        default=None, description="Journal or conference name"
    )
    citation_count: int | None = Field(
        default=None, description="Number of citations"
    )
    source: str | None = Field(
        default=None,
        description="Source database the paper was found in",
        examples=["openalex", "semanticscholar", "crossref"],
    )
    pdf_url: str | None = Field(default=None, description="URL to the PDF")
    pdf_path: str | None = Field(
        default=None, description="Local file path to downloaded PDF"
    )
    is_open_access: bool | None = Field(
        default=None, description="Whether the paper is open access"
    )
    download_status: str | None = Field(
        default=None,
        description="PDF download status",
        examples=["pending", "downloaded", "failed", "not_available"],
    )
    metadata_: dict | None = Field(
        default=None,
        alias="metadata_",
        description="Additional metadata from the source",
    )
    created_at: datetime = Field(..., description="Record creation timestamp")


class PaperList(BaseModel):
    """Schema for paper search results."""

    papers: list[PaperResponse] = Field(..., description="List of papers found")
    total: int = Field(..., ge=0, description="Total number of results")
    sources_searched: list[str] = Field(
        ..., description="Sources that were queried"
    )


class PaperDownloadRequest(BaseModel):
    """Schema for requesting a paper PDF download."""

    paper_id: int = Field(..., description="ID of the paper to download")
    email: str | None = Field(
        default=None,
        description="Email for Unpaywall polite pool access",
        examples=["researcher@university.edu"],
    )


class PaperExtractionResponse(BaseModel):
    """Schema for extracted content from a paper PDF."""

    paper_id: int = Field(..., description="ID of the source paper")
    title: str | None = Field(default=None, description="Extracted title")
    abstract: str | None = Field(default=None, description="Extracted abstract")
    sections: list[dict] | None = Field(
        default=None,
        description="Extracted sections with heading and body text",
    )
    references: list[dict] | None = Field(
        default=None,
        description="Parsed reference entries",
    )
    figures: list[dict] | None = Field(
        default=None,
        description="Extracted figure metadata and captions",
    )
    tables: list[dict] | None = Field(
        default=None,
        description="Extracted table data",
    )


class LiteratureMatrixRequest(BaseModel):
    """Schema for generating a literature comparison matrix."""

    paper_ids: list[int] = Field(
        ...,
        min_length=2,
        description="IDs of papers to compare",
    )
    criteria: list[str] | None = Field(
        default=None,
        description="Comparison criteria / column headings",
        examples=[["method", "dataset", "accuracy", "year"]],
    )


class LiteratureMatrixResponse(BaseModel):
    """Schema for the generated literature comparison matrix."""

    matrix: list[dict] = Field(
        ..., description="Matrix rows, one per paper with criteria columns"
    )
    criteria: list[str] = Field(
        ..., description="Criteria used as column headings"
    )
    papers: list[dict] = Field(
        ..., description="Summary info for each paper in the matrix"
    )
