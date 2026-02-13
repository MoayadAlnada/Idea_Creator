import sys
import os
import shutil
import asyncio
from pathlib import Path

# Explicitly set path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import ONLY what is needed
from core.qa import QA
from utils.logger import setup_logger

logger = setup_logger("simple_verify")

async def main():
    print(">>> SIMPLIFIED VERIFICATION <<<")
    
    asset_path = Path(r"d:\mybestie\data\assets\quickai_ideas")
    if not asset_path.exists():
        print("Asset not found!")
        return

    qa = QA()
    
    # TEST 1: Normal QA
    print(f"\nrunning QA on {asset_path}...")
    result = await qa.test_asset(asset_path)
    if result.passed:
        print("✅ Safe Mode QA Passed.")
    else:
        print(f"❌ Safe Mode QA Failed: {result.issues}")

    # TEST 2: Fail Fast
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

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
