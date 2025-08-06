import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# Ensure directories exist
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Validate API key
if not GEMINI_API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY not found in environment variables")
    print("Please create a .env file with your API key")
