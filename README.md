# Fashion CAD Prompt Creator

Small helper to choose pre-set tones and Kansei words and generate an image prompt
for CAD-style fashion sketches using Gemini.

Quick start

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Configure your Gemini API key by setting the environment variable `GEMINI_API_KEY`
   or creating a `.env` file with `API_KEY=...` in the project root.

3. Run the interactive creator:

```powershell
python tools\create_prompt.py
```

The script will optionally call Gemini and write a `last_image_prompt.txt`.
