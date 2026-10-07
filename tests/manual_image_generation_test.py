import base64
from pathlib import Path

from openai import OpenAI

from backend.app.core.config import OPENAI_API_KEY


def main():
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = """
Create a high-end architectural visualization concept for a contemporary
luxury villa in Dubai.

The villa should have:
- clean modern geometric architecture
- large floor-to-ceiling glass openings
- warm natural stone facade
- elegant landscaping
- a sophisticated entrance
- subtle warm evening lighting
- premium realistic architectural visualization style

This is a conceptual design visualization, not a technical construction drawing.
Do not include text, labels, dimensions, people, logos, or watermarks.
"""

    print("Generating architectural concept...")
    print("This may take a little while.")

    response = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1024x1024",
        quality="low",
        output_format="png",
    )

    if not response.data:
        raise RuntimeError("Image generation returned no data.")

    image_base64 = response.data[0].b64_json

    if not image_base64:
        raise RuntimeError(
            "Image generation returned no base64 image data."
        )

    output_directory = (
        Path(__file__).resolve().parents[1]
        / "generated"
        / "visuals"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_directory
        / "architectural_concept_smoke_test.png"
    )

    image_bytes = base64.b64decode(image_base64)

    output_path.write_bytes(image_bytes)

    print("\n==============================")
    print("IMAGE GENERATION SUCCESSFUL")
    print("==============================")
    print(f"\nSaved image to:")
    print(output_path)
    print(f"\nFile size: {len(image_bytes):,} bytes")


if __name__ == "__main__":
    main()