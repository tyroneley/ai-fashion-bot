import os

from google import genai


def _load_api_key():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("API_KEY")
    if api_key:
        return api_key

    # look for .env next to this file or in cwd
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    env_path = os.path.normpath(env_path)
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    if k.strip() in ('GEMINI_API_KEY', 'API_KEY'):
                        return v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass

    return None


def get_genai_client():
    """Return a configured genai Client. Raises RuntimeError if API key missing."""
    api_key = _load_api_key()
    if not api_key:
        raise RuntimeError(
            "Missing Gemini API key. Set 'GEMINI_API_KEY' env var or add 'API_KEY=...' in .env"
        )
    return genai.Client(api_key=api_key)
