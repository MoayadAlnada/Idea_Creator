import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from utils.logger import setup_logger

logger = setup_logger("config")

# Load environment variables
load_dotenv(override=True)

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = DATA_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"
MEMORY_FILE = DATA_DIR / "memory.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# --- Feature Flags ---
def get_bool_env(key, default=False):
    return os.getenv(key, str(default)).lower() in ("true", "1", "yes")

# Default: Validation ON, AI ON, Publishing OFF (Safe Mode)
ENABLE_AI = get_bool_env("ENABLE_AI", True)
ENABLE_VALIDATION = get_bool_env("ENABLE_VALIDATION", True)
ENABLE_PUBLISH_GITHUB = get_bool_env("ENABLE_PUBLISH_GITHUB", False)
ENABLE_PUBLISH_LEMONSQUEEZY = get_bool_env("ENABLE_PUBLISH_LEMONSQUEEZY", False)
ENABLE_REDDIT_SCAN = get_bool_env("ENABLE_REDDIT_SCAN", False)

# --- API Keys & Mandatory Checks ---
MISSING_KEYS = []

STRICT_PUBLISH_MODE = get_bool_env("STRICT_PUBLISH_MODE", True)

def get_env_strict(key, required=False):
    val = os.getenv(key, "").strip()
    invalid_values = {"none", "null", "changeme", "your_key_here", ""}
    
    if required and (val.lower() in invalid_values):
        MISSING_KEYS.append(key)
        return None
    
    if val.lower() in invalid_values:
        return None
        
    return val

# Mandatory (Blockers if enabled)
OPENAI_API_KEY = get_env_strict("OPENAI_API_KEY", required=ENABLE_AI)
SERPER_API_KEY = get_env_strict("SERPER_API_KEY", required=ENABLE_VALIDATION)

# Optional (Features disabled if missing, but flags might verify them)
# If Strict Mode is ON, these become Mandatory if their feature is enabled.
GITHUB_TOKEN = get_env_strict("GITHUB_PERSONAL_ACCESS_TOKEN", required=(ENABLE_PUBLISH_GITHUB and STRICT_PUBLISH_MODE))
GUMROAD_APP_ID = os.getenv("GUMROAD_APP_ID")         # Legacy/Optional
LEMONSQUEEZY_API_KEY = get_env_strict("LEMONSQUEEZY_API_KEY", required=(ENABLE_PUBLISH_LEMONSQUEEZY and STRICT_PUBLISH_MODE))
REDDIT_CLIENT_ID = get_env_strict("REDDIT_CLIENT_ID", required=(ENABLE_REDDIT_SCAN and STRICT_PUBLISH_MODE))
REDDIT_CLIENT_SECRET = get_env_strict("REDDIT_CLIENT_SECRET", required=(ENABLE_REDDIT_SCAN and STRICT_PUBLISH_MODE))

# Exit if mandatory keys are missing
if MISSING_KEYS:
    logger.error(f"CRITICAL: Missing mandatory environment variables for enabled features: {MISSING_KEYS}")
    sys.exit(1)

# System Constants
MODEL_NAME = "gpt-4-turbo-preview"
FAST_MODEL_NAME = "gpt-3.5-turbo"
MAX_RETRIES = 3
RETRY_DELAY = 2
LOG_LEVEL = "INFO"
