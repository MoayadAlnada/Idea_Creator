import os
import sys

# Mock Env
os.environ["ENABLE_AI"] = "false"
os.environ.pop("OPENAI_API_KEY", None)

try:
    print("Importing utils.api_client with no key...")
    import utils.api_client
    print("Import success.")
except Exception as e:
    print(f"Import FAILED: {e}")
    sys.exit(1)
