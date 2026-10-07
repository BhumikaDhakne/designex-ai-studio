import base64
import uuid
from pathlib import Path

from openai import OpenAI

from backend.app.core.config import OPENAI_API_KEY
from backend.app.schemas.visual import (
    VisualGenerationRequest,
    VisualGenerationResponse,
    VisualRefinementRequest,
)


class VisualGenerationService:
    """Handles AI-powered architectural concept generation."""

    MODEL = "gpt-image-2"

    SIZE_MAP = {
        "square": "1024x1024",
        "portrait": "1024x1536",
        "landscape": "1536x1024",
    }

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

        self.output_directory = (
            Path(__file__).resolve().parents[3]
            / "generated"
            / "visuals"
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def build_prompt(
        self,
        request: VisualGenerationRequest,
    ) -> str:
        """Build a controlled architectural visualization prompt."""

        return f"""
Create a high-end architectural visualization concept.

Project:
{request.project_name}

Project type:
{request.project_type}

Location:
{request.location}

Design brief:
{request.design_brief}

Visual style:
{request.visual_style}

Time of day:
{request.time_of_day}

Requirements:
- Create a coherent architectural concept based on the project brief.
- Prioritize realistic architectural proportions and materials.
- Show the building and surrounding environment clearly.
- Use premium architectural visualization quality.
- Reflect the specified location and design context where appropriate.
- Create a polished presentation suitable for early-stage design ideation.
- Do not include text, labels, dimensions, logos, watermarks, or UI elements.
- This is a conceptual visualization, not a technical construction drawing.
""".strip()

    def _save_image(
        self,
        image_base64: str,
        generation_id: str,
    ) -> Path:
        """Decode and save generated image."""

        image_bytes = base64.b64decode(
            image_base64
        )

        output_path = (
            self.output_directory
            / f"{generation_id}.png"
        )

        output_path.write_bytes(
            image_bytes
        )

        return output_path

    def generate(
        self,
        request: VisualGenerationRequest,
    ) -> VisualGenerationResponse:
        """Generate a new architectural concept image."""

        prompt = self.build_prompt(request)

        image_size = self.SIZE_MAP[
            request.aspect_ratio
        ]

        response = self.client.images.generate(
            model=self.MODEL,
            prompt=prompt,
            size=image_size,
            quality="low",
            output_format="png",
        )

        if not response.data:
            raise RuntimeError(
                "Image generation returned no data."
            )

        image_base64 = response.data[0].b64_json

        if not image_base64:
            raise RuntimeError(
                "Image generation returned no image data."
            )

        generation_id = str(uuid.uuid4())

        output_path = self._save_image(
            image_base64=image_base64,
            generation_id=generation_id,
        )

        return VisualGenerationResponse(
            generation_id=generation_id,
            project_name=request.project_name,
            prompt=prompt,
            image_url=(
                f"/generated/visuals/"
                f"{generation_id}.png"
            ),
            local_path=str(output_path),
            status="generated",
        )

    def refine(
        self,
        request: VisualRefinementRequest,
    ) -> VisualGenerationResponse:
        """Refine an existing architectural concept."""

        source_path = (
            self.output_directory
            / f"{request.generation_id}.png"
        )

        if not source_path.exists():
            raise FileNotFoundError(
                "The requested visual generation was not found."
            )

        refinement_prompt = f"""
Refine the provided architectural visualization.

Requested refinement:
{request.refinement_instruction}

Important instructions:
- Preserve the overall architectural concept and composition
  where possible.
- Apply the requested design changes clearly.
- Maintain realistic architectural proportions.
- Maintain a premium architectural visualization style.
- Do not add text, labels, dimensions, logos, watermarks,
  or UI elements.
- This remains a conceptual visualization, not a technical
  construction drawing.
""".strip()

        with source_path.open(
            "rb"
        ) as image_file:
            response = self.client.images.edit(
                model=self.MODEL,
                image=image_file,
                prompt=refinement_prompt,
                size="1024x1024",
                quality="low",
                output_format="png",
            )

        if not response.data:
            raise RuntimeError(
                "Image refinement returned no data."
            )

        image_base64 = response.data[0].b64_json

        if not image_base64:
            raise RuntimeError(
                "Image refinement returned no image data."
            )

        generation_id = str(uuid.uuid4())

        output_path = self._save_image(
            image_base64=image_base64,
            generation_id=generation_id,
        )

        return VisualGenerationResponse(
            generation_id=generation_id,
            project_name="Refined Architectural Concept",
            prompt=refinement_prompt,
            image_url=(
                f"/generated/visuals/"
                f"{generation_id}.png"
            ),
            local_path=str(output_path),
            status="generated",
            parent_generation_id=(
                request.generation_id
            ),
        )