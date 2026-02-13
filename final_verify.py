import sys
import os
import shutil
import asyncio
from pathlib import Path

# Explicitly set path to current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import after path fix
try:
    from utils.logger import setup_logger
    from core.qa import QA
except ImportError as e:
    print(f"CRITICAL IMPORT ERROR: {e}")
    sys.exit(1)

logger = setup_logger("final_verify")

async def run_safe_mode_test():
    print("\n>>> TEST 1: SAFE MODE (Flags OFF) <<<")
    
    # 1. Force Env Vars for Safety
    os.environ["ENABLE_PUBLISH_GITHUB"] = "false"
    os.environ["ENABLE_PUBLISH_LEMONSQUEEZY"] = "false"
    os.environ["ENABLE_AI"] = "false"
    # We keep validation enabled to test the QA module itself, but without API calls if possible
    # Actually user asked for "ENABLE_VALIDATION=true"
    os.environ["ENABLE_VALIDATION"] = "true" 
    # But SERPER_API_KEY is mandatory if validation is true.
    # I'll rely on the existing .env or if config.py checks it.
    # config.py performs checks at import time? No, at module level.
    # If I import config, it checks env vars.
    # So I need to set them BEFORE importing config?
    # verify_phase6 didn't import config explicitly, but core.qa -> setup_logger (clean)
    # core.ecosystem -> scanner -> config.
    # So I must set env vars BEFORE importing ecosystem.
    
    # But I can't set them before import if I don't import them...
    # Wait, `os.environ` changes affect subsequent imports if code reads os.environ.
    # `config.py` runs `load_dotenv` which might overwrite `os.environ` if I don't use override?
    # `config.py` has `load_dotenv(override=True)`.
    # So `.env` file wins over `os.environ` set in python script *before* import?
    # Yes, if `load_dotenv(override=True)` is called.
    # So my script CANNOT override .env simply by `os.environ[...] = ...` if `config` reloads .env.
    
    # WORKAROUND: Modify .env temporarily or rely on `config.py` reading from `os.environ`?
    # `load_dotenv` reads file and *updates* os.environ.
    # If `override=True`, it overwrites existing env vars.
    # So I must either:
    # 1. Rename .env so it's not found.
    # 2. Or modify .env.
    pass

async def main():
    # TEST setup: Rename .env to avoid interference
    if os.path.exists(".env"):
        os.rename(".env", ".env.bak")
        print("Renamed .env to .env.bak")
    
    try:
        # Set Up Test Env
        os.environ["OPENAI_API_KEY"] = "sk-dummy"
        os.environ["SERPER_API_KEY"] = "dummy"
        os.environ["ENABLE_PUBLISH_GITHUB"] = "false"
        os.environ["ENABLE_PUBLISH_LEMONSQUEEZY"] = "false"
        os.environ["ENABLE_AI"] = "false"
        os.environ["ENABLE_VALIDATION"] = "true" # "Controlled test" request
        
        # Now import Ecosystem (which imports config, which looks for .env, finds none, uses os.environ)
        from core.ecosystem import Ecosystem
        
        # Run QA directly
        asset_path = Path(r"d:\mybestie\data\assets\quickai_ideas")
        if not asset_path.exists():
            print("Asset not found!")
            return

        qa = QA()
        print(f"Running QA on {asset_path}...")
        result = await qa.test_asset(asset_path)
        
        if result.passed:
            print("✅ Safe Mode QA Passed.")
        else:
            print(f"❌ Safe Mode QA Failed: {result.issues}")

        # FAIL FAST TEST
        print("\n>>> TEST 2: FAIL FAST (Syntax Error Injection) <<<")
        target_file = asset_path / "main.py"
        backup_file = asset_path / "main.py.bak"
        shutil.copy(target_file, backup_file)
        
        try:
            with open(target_file, "a") as f:
                f.write("\nThis is a syntax error because it is just text\n")
            
            print(f"Running QA on compromised asset...")
            result = await qa.test_asset(asset_path)
            
            if not result.passed:
                print("✅ Fail Fast CONFIRMED: QA caught the error.")
                print(f"Issues found: {result.issues}")
            else:
                print("❌ Fail Fast FAILED: QA passed despite syntax error.")
        finally:
            shutil.copy(backup_file, target_file)
            os.remove(backup_file)
            print("Restored main.py.")

    finally:
        if os.path.exists(".env.bak"):
            os.rename(".env.bak", ".env")
            print("Restored .env")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
