"""
Quick start script for the Fashion Design Generator.
Starts both the backend API and serves the frontend.
"""
import os
import sys
import webbrowser
import time
from pathlib import Path

def main():
    # Check if we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("=" * 60)
    print("🎨 AI Fashion Design Generator")
    print("=" * 60)
    print()
    
    # Check for .env file
    env_file = project_root / '.env'
    if not env_file.exists():
        print("⚠️  WARNING: No .env file found!")
        print("   Please create a .env file with your API keys:")
        print("   - GEMINI_API_KEY=your_key_here")
        print("   - HUGGINGFACE_TOKEN=your_token_here (optional)")
        print()
        proceed = input("Continue anyway? (y/N): ").strip().lower()
        if proceed != 'y':
            sys.exit(1)
    
    # Start the backend server
    print("🚀 Starting backend server...")
    print("   Backend API: http://localhost:8000")
    print("   Frontend UI: http://localhost:8000/index.html")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Wait a moment for server to start, then open browser
    import threading
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:8000/index.html')
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start uvicorn server
    os.system('uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload')

if __name__ == '__main__':
    main()
