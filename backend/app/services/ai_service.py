from openai import OpenAI

from backend.app.core.config import OPENAI_API_KEY


class AIService:
    """Handles communication with the OpenAI API."""

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def test_connection(self) -> str:
        response = self.client.responses.create(
            model="gpt-5.5",
            input="Respond with exactly: Designex AI connection successful.",
        )

        return response.output_text