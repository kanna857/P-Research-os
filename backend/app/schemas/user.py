"""User-related Pydantic v2 schemas for authentication and profile management."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: str = Field(
        ...,
        description="User's email address",
        examples=["researcher@university.edu"],
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username",
        examples=["jsmith"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password (min 8 characters)",
        examples=["SecureP@ss123"],
    )
    full_name: str | None = Field(
        default=None,
        max_length=100,
        description="User's full name",
        examples=["Jane Smith"],
    )


class UserLogin(BaseModel):
    """Schema for user login."""

    email: str = Field(
        ...,
        description="Registered email address",
        examples=["researcher@university.edu"],
    )
    password: str = Field(
        ...,
        description="Account password",
        examples=["SecureP@ss123"],
    )


class UserResponse(BaseModel):
    """Schema for user data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")
    full_name: str | None = Field(default=None, description="User's full name")
    is_active: bool = Field(default=True, description="Whether the account is active")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime | None = Field(
        default=None, description="Last profile update timestamp"
    )


class Token(BaseModel):
    """Schema for JWT authentication token response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(
        default="bearer",
        description="Token type",
        examples=["bearer"],
    )
