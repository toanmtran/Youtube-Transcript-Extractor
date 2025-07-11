import os
import sys
from dotenv import load_dotenv

# Finds the .env file and loads its variables so os.getenv() can access them.
load_dotenv()

# Determine the base directory of the project
if getattr(sys, 'frozen', False):
    basedir = sys._MEIPASS
else:
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# --- API Keys ---
# os.getenv() reads a variable and returns None if the key is not found.
YOUTUBE_DATA_API_KEY = os.getenv("YOUTUBE_DATA_API_KEY")
GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

# --- File Paths ---
GOOGLE_DOCS_CREDENTIALS_PATH = os.path.join(basedir, "credentials", "Google-Docs-API-credentials.json")

# --- AI Model Configuration ---
HF_ASR_MODEL = "openai/whisper-large-v3"
GEMINI_MODEL_NAME = "gemini-1.5-flash"

# --- Constants ---
MAX_SHORT_DURATION_SECONDS = 60