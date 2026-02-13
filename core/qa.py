import ast
import os
import subprocess
import asyncio
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger("qa")

class QAResult:
    def __init__(self, passed: bool, issues: list):
        self.passed = passed
        self.issues = issues

class QA:
    def __init__(self):
        pass

    async def run_command(self, cmd: list, cwd: Path) -> tuple[bool, str]:
        """Runs a shell command and returns success status and output."""
        try:
            # Use shell=True for Windows compatibility with npm/python
            proc = await asyncio.create_subprocess_shell(
                " ".join(cmd),
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            success = proc.returncode == 0
            msg = stdout.decode().strip() + "\n" + stderr.decode().strip()
            return success, msg
        except Exception as e:
            return False, str(e)

    async def test_asset(self, asset_path: Path) -> QAResult:
        """
        Runs comprehensive QA checks:
        1. Empty file checks
        2. Python Syntax (compileall)
        3. Python Linting (flake8 - if installed)
        4. Frontend Build (npm install && npm run build - if package.json exists)
        """
        logger.info(f"Running Strict QA on {asset_path}")
        issues = []
        
        # 1. basic File Checks
        if not (asset_path / "README.md").exists():
            issues.append("Missing README.md")
            
        for file in asset_path.rglob("*"):
            if file.is_file() and file.stat().st_size == 0:
                issues.append(f"Empty file: {file.name}")

        # 2. Python Checks
        py_files = list(asset_path.rglob("*.py"))
        if py_files:
            # A. CompileAll (Syntax Check)
            success, output = await self.run_command(["python", "-m", "compileall", "-q", "."], cwd=asset_path)
            if not success:
                issues.append(f"Python Syntax Errors:\n{output}")
            
            # B. Flake8 (Linting) - Optional, only if installed
            # We explicitly try to run it, but don't fail if command not found, only if linting fails
            success, output = await self.run_command(["python", "-m", "flake8", ".", "--count", "--select=E9,F63,F7,F82", "--show-source", "--statistics"], cwd=asset_path)
            # We catch specific critical errors (E9 syntax, F63/F7 logic, F82 undefined)
            if not success and "command not found" not in output:
                 issues.append(f"Linting Errors:\n{output}")

        # 3. Frontend Checks
        if (asset_path / "frontend_app" / "package.json").exists():
            logger.info("Detected Frontend. Running Build Check...")
            frontend_dir = asset_path / "frontend_app"
            
            # npm install
            success, output = await self.run_command(["npm", "install"], cwd=frontend_dir)
            if not success:
                issues.append(f"Frontend Install Failed:\n{output[-500:]}") # Last 500 chars
            else:
                # npm run build
                success, output = await self.run_command(["npm", "run", "build"], cwd=frontend_dir)
                if not success:
                    issues.append(f"Frontend Build Failed:\n{output[-500:]}")

        passed = len(issues) == 0
        status_str = 'PASS' if passed else 'FAIL'
        logger.info(f"QA Result: {status_str} ({len(issues)} issues)")
        
        return QAResult(passed, issues)
