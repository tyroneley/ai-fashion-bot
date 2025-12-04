"""CLI to generate fashion designs with image generation.

Usage: python tools/generate_design.py <sketch_image_path>
"""
import sys
import os
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app.tones import TONES, KANSEI_WORDS
from backend.app.generator import build_gemini_instruction, call_gemini_for_prompt, refine_for_image_model


def pick_from_list(title, options, max_selections=None):
    print(f"\n{title}")
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")
    
    if max_selections:
        prompt_text = f"Select comma-separated numbers (max {max_selections}, or press Enter to skip): "
    else:
        prompt_text = "Select comma-separated numbers (or press Enter to skip): "
    
    raw = input(prompt_text).strip()
    if not raw:
        return []
    try:
        picks = [int(x.strip()) for x in raw.split(',') if x.strip()]
        selected = [options[i-1] for i in picks if 1 <= i <= len(options)]
        
        if max_selections and len(selected) > max_selections:
            print(f"Too many selections! Maximum is {max_selections}. Try again.")
            return pick_from_list(title, options, max_selections)
        
        return selected
    except Exception:
        print("Invalid selection. Try again.")
        return pick_from_list(title, options, max_selections)


def main():
    print("="*60)
    print("Fashion Design Generator - CLI Version")
    print("="*60)
    
    # Get sketch path
    if len(sys.argv) > 1:
        sketch_path = Path(sys.argv[1])
    else:
        sketch_input = input("\nEnter path to your sketch image: ").strip()
        sketch_path = Path(sketch_input)
    
    if not sketch_path.exists():
        print(f"Error: Sketch file not found at {sketch_path}")
        sys.exit(1)
    
    print(f"\n✓ Using sketch: {sketch_path}")
    
    # Select tones and Kansei words
    print("\n" + "="*60)
    tones = pick_from_list("Available Tones (select up to 3):", TONES, max_selections=3)
    kansei = pick_from_list("Available Kansei words (select any):", KANSEI_WORDS)
    
    if not tones and not kansei:
        print("\nError: Please select at least one tone or Kansei word.")
        sys.exit(1)
    
    print(f"\n✓ Selected tones: {', '.join(tones) if tones else 'None'}")
    print(f"✓ Selected Kansei words: {', '.join(kansei) if kansei else 'None'}")
    
    # Generate prompt with Gemini
    print("\n" + "="*60)
    print("Generating prompt with Gemini AI...")
    print("="*60)
    
    try:
        instruction = build_gemini_instruction(tones, kansei)
        gemini_text = call_gemini_for_prompt(instruction)
        image_prompt = refine_for_image_model(gemini_text)
        
        print("\n--- Generated Prompt ---")
        print(image_prompt)
        print()
    except Exception as e:
        print(f"\nError generating prompt: {e}")
        sys.exit(1)
    
    # Generate image
    print("="*60)
    print("Generating image with Stable Diffusion + ControlNet...")
    print("="*60)
    
    try:
        # Import here to catch errors
        from backend.app.image_generator import generate_fashion_design
        
        output_path = PROJECT_ROOT / "backend" / "media" / "generated" / f"cli_generated_{sketch_path.stem}.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\nProcessing... This may take a few minutes...")
        print(f"Input: {sketch_path}")
        print(f"Output: {output_path}")
        
        generate_fashion_design(
            sketch_path=sketch_path,
            prompt=image_prompt,
            output_path=output_path,
            num_inference_steps=20,
            guidance_scale=7.5,
            controlnet_conditioning_scale=1.0,
        )
        
        print(f"\n✓ Success! Generated image saved to:")
        print(f"  {output_path}")
        
        # Save prompt too
        prompt_path = output_path.with_suffix('.txt')
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(f"Tones: {', '.join(tones)}\n")
            f.write(f"Kansei Words: {', '.join(kansei)}\n\n")
            f.write(f"Generated Prompt:\n{image_prompt}")
        print(f"✓ Prompt saved to:")
        print(f"  {prompt_path}")
        
    except ImportError as e:
        print(f"\nError: Could not load image generation dependencies.")
        print(f"Details: {e}")
        print("\nThis is likely due to PyTorch not being properly installed.")
        print("The prompt has been generated but image generation is unavailable.")
        
        # Save prompt anyway
        prompt_path = Path(PROJECT_ROOT) / "last_image_prompt.txt"
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(image_prompt)
        print(f"\n✓ Prompt saved to: {prompt_path}")
        print("\nYou can use this prompt with other image generation tools.")
        
    except Exception as e:
        print(f"\nError during image generation: {e}")
        print("\nThe prompt was generated successfully but image generation failed.")
        
        # Save prompt anyway
        prompt_path = Path(PROJECT_ROOT) / "last_image_prompt.txt"
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(image_prompt)
        print(f"\n✓ Prompt saved to: {prompt_path}")


if __name__ == '__main__':
    main()
