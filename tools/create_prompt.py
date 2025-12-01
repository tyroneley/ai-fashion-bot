"""Interactive CLI to choose tones/Kansei words and create prompts using Gemini.

Usage: python tools/create_prompt.py
"""
import sys
import os

# Ensure project root is on sys.path so `backend` package can be imported
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app.tones import TONES, KANSEI_WORDS
from backend.app.generator import build_gemini_instruction, call_gemini_for_prompt, refine_for_image_model


def pick_from_list(title, options):
    print(f"\n{title}")
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")
    raw = input("Select comma-separated numbers (or press Enter to skip): ").strip()
    if not raw:
        return []
    try:
        picks = [int(x.strip()) for x in raw.split(',') if x.strip()]
        return [options[i-1] for i in picks if 1 <= i <= len(options)]
    except Exception:
        print("Invalid selection. Try again.")
        return pick_from_list(title, options)


def main():
    print("Fashion CAD Prompt Creator — choose tones and Kansei words")
    tones = pick_from_list("Available Tones:", TONES)
    kansei = pick_from_list("Available Kansei words:", KANSEI_WORDS)

    instruction = build_gemini_instruction(tones, kansei)
    print("\n--- Instruction sent to Gemini ---\n")
    print(instruction)

    proceed = input("Call Gemini to generate image prompt now? (y/N): ").strip().lower()
    if proceed != 'y':
        print("Cancelled Gemini call — instruction saved to stdout.")
        sys.exit(0)

    print("Calling Gemini... this requires a configured GEMINI_API_KEY or API_KEY in .env")
    gemini_text = call_gemini_for_prompt(instruction)
    print("\n--- Gemini Output ---\n")
    print(gemini_text)

    image_prompt = refine_for_image_model(gemini_text)
    print("\n--- Final Image Prompt (for image model) ---\n")
    print(image_prompt)

    save = input("Save the final image prompt to 'last_image_prompt.txt'? (Y/n): ").strip().lower()
    if save != 'n':
        with open('last_image_prompt.txt', 'w', encoding='utf-8') as f:
            f.write(image_prompt)
        print("Saved to last_image_prompt.txt")


if __name__ == '__main__':
    main()
