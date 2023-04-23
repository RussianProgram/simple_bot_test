import os
from dotenv import load_dotenv

load_dotenv()

# Set up API keys
BOT_TOKEN = os.getenv("BOT_TOKEN")
CONVERTER_API_KEY = os.getenv("CONVERTER_API_KEY")
