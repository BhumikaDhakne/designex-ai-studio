from typing import Literal

from pydantic import BaseModel, Field


ContentStatus = Literal[
    "PENDING_APPROVAL",
    "APPROVED",
    "READY_TO_PUBLISH",
]


class ContentGenerationRequest(BaseModel):
    project_name: str = Field(
        min_length=1,
        max_length=200,
    )

    project_type: str = Field(
        min_length=1,
        max_length=100,
    )

    location: str = Field(
        min_length=1,
        max_length=200,
    )

    project_description: str = Field(
        min_length=10,
        max_length=3000,
    )

    target_audience: str = Field(
        min_length=5,
        max_length=1000,
    )

    platform: Literal[
        "facebook",
        "both",
    ] = "both"

    whatsapp_cta: str = Field(
        default=(
            "Contact us on WhatsApp to discuss "
            "your next project."
        ),
        max_length=300,
    )


class FacebookContent(BaseModel):
    headline: str
    caption: str
    call_to_action: str
    hashtags: list[str]


class LinkedInContent(BaseModel):
    headline: str
    caption: str
    call_to_action: str
    hashtags: list[str]


class AIContentDraft(BaseModel):
    """
    Structured output expected directly from the AI model.
    Application metadata is added by the backend separately.
    """

    content_strategy: str

    facebook: FacebookContent

    linkedin: LinkedInContent


class ContentGenerationResponse(BaseModel):
    generation_id: str

    project_name: str

    target_audience: str

    content_strategy: str

    facebook: FacebookContent

    linkedin: LinkedInContent

    status: ContentStatus

    approved_at: str | None = None