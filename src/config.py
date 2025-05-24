import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

HF_TOKEN = os.getenv("HF_TOKEN")
IMG_DESC_API_KEY = os.getenv("IMG_DESC_API_KEY")

DATA_INPUT_PATH = os.getenv("DATA_INPUT_PATH", "data/input/")
DATA_OUTPUT_PATH = os.getenv("DATA_OUTPUT_PATH", "data/output/"