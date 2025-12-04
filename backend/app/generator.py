"""Build prompts using preset tones/Kansei words and Gemini."""
from typing import List

from .tones import TONES, KANSEI_WORDS
from .llm_client import get_genai_client


def build_gemini_instruction(selected_tones: List[str], selected_kansei: List[str]) -> str:
    """Construct an instruction for Gemini to expand into a detailed image prompt.

    The instruction asks Gemini to produce a concise but highly-detailed image prompt
    suited for CAD-style fashion sketches with technical annotations.
    """
    tone_clause = ", ".join(selected_tones) if selected_tones else ""
    kansei_clause = ", ".join(selected_kansei) if selected_kansei else ""

    instructions = (
        f"You are a prompt engineer for fashion CAD-style sketch generation. "
        f"Given the following selected tones: {tone_clause}. "
        f"And the following Kansei (sensory/feeling) keywords: {kansei_clause}. "
        "Produce a single, compact image-generation prompt (1-2 paragraphs, 2-4 sentences) "
        "that an image model can use to create a CAD-style technical sketch of a fashion garment. If given an image, use the image as a reference."
        "Include: silhouette, garment type, material suggestions, notable construction details, "
        "stitching/topstitching, seam placement, recommended line weights, front/side/back views, "
        "a short palette, and any annotations/measurements that help a patternmaker. "
        "Prioritize clarity and technical cues; keep creative tone influenced by the selected tones."
    )

    return instructions


def call_gemini_for_prompt(instruction: str, model: str = "gemini-2.5-flash") -> str:
    client = get_genai_client()
    response = client.models.generate_content(model=model, contents=instruction)
    # The API returns text on .text (earlier script used response.text)
    return getattr(response, 'text', str(response))


def refine_for_image_model(gemini_text: str) -> str:
    """Optionally transform the Gemini output into a final image prompt for the image model.

    For simplicity, we return Gemini's text but append tags guiding 'CAD-style', 'line art',
    and technical annotations. This can be tailored to particular image backends later.
    """
    suffix = (
        " --output_format: CAD-style technical line drawing; monochrome or single-color palette; "
        "high-contrast line art; include front/side/back views; numbered annotations for seams and measurements; "
        "no photographic textures; focus on construction and pattern clarity."
    )
    return gemini_text.strip() + "\n" + suffix
