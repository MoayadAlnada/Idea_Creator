import os
import sys
import subprocess

# Define test cases
# 1. Whitespace Key -> Should be treated as missing
# 2. Strict Mode True, Token Missing -> Startup Crash (Config check) or Runtime Error
# 3. Strict Mode False, Token Missing -> Runtime Skip

def run_test_case(name, env_vars, expected_output_substr, description):
    print(f"\n>>> TEST: {name} ({description})")
    print(f"    Env: {env_vars}")
    
    # Run a script that imports config and publisher
    script = """
import os
import sys
from pathlib import Path

try:
    import config
    print(f"Config Loaded. Strict: {config.STRICT_PUBLISH_MODE}")
    from core.publisher import Publisher
    import asyncio
    
    async def run():
        p = Publisher()
        # Mock metadata
        meta = {'title': 'Test', 'description': 'desc'}
        # Try publish (will use env vars)
        if config.ENABLE_PUBLISH_GITHUB:
            await p.publish_to_github(Path('.'), meta)
        if config.ENABLE_PUBLISH_LEMONSQUEEZY:
            await p.publish_to_lemonsqueezy(meta, 'http://repo')

    asyncio.run(run())
except SystemExit as e:
    print(f"SystemExit: {e}")
except Exception as e:
    print(f"RuntimeError: {e}")
"""
    # Environment for subprocess
    env = os.environ.copy()
    env.update(env_vars)
    
    # Fix python path
    env["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))

    result = subprocess.run(
        [sys.executable, "-c", script],
        env=env,
        capture_output=True,
        text=True
    )
    
    output = result.stdout + result.stderr
    if expected_output_substr in output:
        print("    ✅ PASSED")
    else:
        print("    ❌ FAILED")
        print("    Output preview:", output[:200].replace('\n', ' '))


if __name__ == "__main__":
    # Test 1: Placeholder Value (Strict Mode TRUE) -> Should Fail Config or Runtime
    # With strict mode TRUE, config.py checks required=True.
    # So "   " should cause MISSING_KEYS and SystemExit(1)
    run_test_case(
        "Placeholder/Whitespace Rejection (Strict=True)",
        {
            "ENABLE_PUBLISH_GITHUB": "true",
            "STRICT_PUBLISH_MODE": "true",
            "GITHUB_PERSONAL_ACCESS_TOKEN": "   ", # Whitespace
        },
        "CRITICAL: Missing mandatory environment variables",
        "Should crash at config load due to missing keys"
    )

    # Test 2: Placeholder Value (Strict Mode FALSE) -> Should Skip
    # With strict mode FALSE, config.py checks required=False.
    # So GITHUB_TOKEN is None. Config loads.
    # Publisher sees None. publish_to_github calls... warns and skips.
    run_test_case(
        "Placeholder/Whitespace Rejection (Strict=False)",
        {
            "ENABLE_PUBLISH_GITHUB": "true",
            "STRICT_PUBLISH_MODE": "false",
            "GITHUB_PERSONAL_ACCESS_TOKEN": "your_key_here", # Placeholder
        },
        "Skipping (Strict Mode OFF)",
        "Should load config but skip publish with warning"
    )
    
    # Test 3: Valid Token (Strict=True) -> Should Attempt Publish (Fail auth obviously, but pass checks)
    # We expect "Bad credentials" or similar from Github, OR "Failed: ..." logged by publisher
    # But NOT "Missing mandatory..."
    run_test_case(
        "Valid-looking Key (Strict=True)",
        {
            "ENABLE_PUBLISH_GITHUB": "true",
            "STRICT_PUBLISH_MODE": "true",
            "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_personal_access_token_here",
        },
        "GitHub Publish Failed", # Likely 401 Bad Credentials
        "Should pass config and strict check, then fail at API level"
    )

