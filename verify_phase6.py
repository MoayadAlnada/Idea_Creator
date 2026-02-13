import os
import sys
import shutil
from pathlib import Path
import asyncio

# Add root to sys.path
root_dir = str(Path(__file__).parent.resolve())
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    print("Importing utils.logger...")
    from utils.logger import setup_logger
    print("Importing core.qa...")
    from core.qa import QA
    print("Importing core.ecosystem...")
    from core.ecosystem import Ecosystem
    print("Imports successful.")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)

logger = setup_logger("verify_phase6")

async def run_safe_mode_test():
    logger.info(">>> TEST 1: SAFE MODE (Flags OFF) <<<")
    
    # 1. Force Env Vars for Safety
    os.environ["ENABLE_PUBLISH_GITHUB"] = "false"
    os.environ["ENABLE_PUBLISH_LEMONSQUEEZY"] = "false"
    os.environ["ENABLE_AI"] = "false"
    os.environ["ENABLE_VALIDATION"] = "false" # Skip for this test to be fast
    
    # 2. Run QA Execution directly on existing asset
    asset_path = Path(r"d:\mybestie\data\assets\quickai_ideas")
    if not asset_path.exists():
        logger.error(f"Asset not found at {asset_path}")
        return

    qa = QA()
    logger.info(f"Running QA on {asset_path}...")
    result = await qa.test_asset(asset_path)
    
    if result.passed:
        logger.info("✅ Safe Mode QA Passed.")
    else:
        logger.error(f"❌ Safe Mode QA Failed: {result.issues}")

async def run_fail_fast_test():
    logger.info("\n>>> TEST 2: FAIL FAST (Syntax Error Injection) <<<")
    
    asset_path = Path(r"d:\mybestie\data\assets\quickai_ideas")
    target_file = asset_path / "main.py"
    backup_file = asset_path / "main.py.bak"
    
    # Backup
    shutil.copy(target_file, backup_file)
    
    try:
        # Inject Syntax Error
        with open(target_file, "a") as f:
            f.write("\nThis is a syntax error because it is just text\n")
            
        qa = QA()
        logger.info(f"Running QA on compromised asset...")
        result = await qa.test_asset(asset_path)
        
        if not result.passed:
            logger.info("✅ Fail Fast CONFIRMED: QA caught the error.")
            logger.info(f"Issues found: {result.issues}")
        else:
            logger.error("❌ Fail Fast FAILED: QA passed despite syntax error.")
            
    finally:
        # Restore
        shutil.copy(backup_file, target_file)
        os.remove(backup_file)
        logger.info("Restored main.py.")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_safe_mode_test())
    loop.run_until_complete(run_fail_fast_test())
