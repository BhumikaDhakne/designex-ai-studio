import uuid
from datetime import datetime, timezone

from openai import OpenAI

from backend.app.core.config import OPENAI_API_KEY
from backend.app.schemas.content import (
    AIContentDraft,
    ContentGenerationRequest,
    ContentGenerationResponse,
)


class ContentGenerationService:
    """Handles AI-powered marketing content generation."""

    MODEL = "gpt-5.5"

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

        self.generated_content: dict[
            str,
            ContentGenerationResponse,
        ] = {}

    def build_instructions(self) -> str:
        return """
You are the AI Content Studio for a premium architecture,
interior design, landscape and project management company.

Your task is to transform project information into useful,
platform-specific marketing content.

IMPORTANT RULES:

- Use only information provided in the project input.
- Do not invent project facts.
- Do not invent awards, certifications, project values,
  completion dates, client names, or performance claims.
- Do not claim that a project is completed unless the input
  explicitly says so.
- Keep the content appropriate for a premium design and
  architecture brand.
- Facebook should be visually engaging and audience-oriented.
- LinkedIn should be more professional and project-story oriented.
- The content should communicate the design value of the project.
- Use the supplied target audience when deciding the messaging.
- Include a clear but natural call to action.
- Use the supplied WhatsApp CTA where appropriate.
- Hashtags should be relevant and limited.
- Avoid exaggerated claims.
- Avoid generic filler language.
- Do not mention that AI generated the content.

Return only the requested structured content.
"""

    def generate(
        self,
        request: ContentGenerationRequest,
    ) -> ContentGenerationResponse:
        """Generate platform-specific marketing content."""

        input_text = f"""
PROJECT INFORMATION

Project name:
{request.project_name}

Project type:
{request.project_type}

Location:
{request.location}

Project description:
{request.project_description}


TARGET AUDIENCE

{request.target_audience}


WHATSAPP CTA

{request.whatsapp_cta}


PLATFORM REQUIREMENT

Generate content for:
{request.platform}


CONTENT REQUIREMENTS

Create:

1. Content strategy
   - Explain the audience angle.
   - Explain the messaging approach.
   - Keep it concise and practical.

2. Facebook content
   - headline
   - engaging caption
   - call to action
   - relevant hashtags

3. LinkedIn content
   - professional headline
   - professional caption
   - call to action
   - relevant hashtags
"""

        response = self.client.responses.parse(
            model=self.MODEL,
            instructions=self.build_instructions(),
            input=input_text,
            text_format=AIContentDraft,
        )

        if response.output_parsed is None:
            raise RuntimeError(
                "AI returned no structured content."
            )

        draft = response.output_parsed

        generation_id = str(uuid.uuid4())

        result = ContentGenerationResponse(
            generation_id=generation_id,
            project_name=request.project_name,
            target_audience=request.target_audience,
            content_strategy=draft.content_strategy,
            facebook=draft.facebook,
            linkedin=draft.linkedin,
            status="PENDING_APPROVAL",
            approved_at=None,
        )

        self.generated_content[
            generation_id
        ] = result

        return result

    def approve(
        self,
        generation_id: str,
    ) -> ContentGenerationResponse:
        """Approve generated content for simulated publishing."""

        content = self.generated_content.get(
            generation_id
        )

        if content is None:
            raise KeyError(
                f"Content generation not found: {generation_id}"
            )

        approved_at = datetime.now(
            timezone.utc
        ).isoformat()

        content.status = "APPROVED"
        content.approved_at = approved_at

        # Publishing is intentionally simulated
        # because Designex Meta credentials are unavailable.
        content.status = "READY_TO_PUBLISH"

        return content