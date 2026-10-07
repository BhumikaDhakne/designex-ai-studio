from typing import Literal

from pydantic import BaseModel, Field


class VisualGenerationRequest(BaseModel):
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

    design_brief: str = Field(
        min_length=10,
        max_length=3000,
    )

    visual_style: str = Field(
        default="Photorealistic architectural visualization",
        max_length=200,
    )

    time_of_day: str = Field(
        default="Golden hour",
        max_length=100,
    )

    aspect_ratio: Literal[
        "square",
        "portrait",
        "landscape",
    ] = "square"


class VisualRefinementRequest(BaseModel):
    generation_id: str = Field(
        min_length=1,
        max_length=100,
    )

    refinement_instruction: str = Field(
        min_length=5,
        max_length=2000,
    )


class VisualGenerationResponse(BaseModel):
    generation_id: str
    project_name: str
    prompt: str
    image_url: str
    local_path: str
    status: Literal[
        "generated",
        "failed",
    ]

    parent_generation_id: str | None = None