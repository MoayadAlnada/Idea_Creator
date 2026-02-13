import asyncio
from pathlib import Path
from utils.logger import setup_logger
from utils.api_client import api_client
from core.planner import BuildPlan, FileTask
from config import ASSETS_DIR

logger = setup_logger("builder")

class Builder:
    def __init__(self):
        pass

    async def generate_file_content(self, task: FileTask, plan: BuildPlan) -> str:
        """
        Generates content for a single file.
        """
        logger.info(f"Building file: {task.filename}")
        
        system_prompt = f"""
        You are an expert developer. Write the content for the file '{task.filename}'.
        
        Project Context:
        Title: {plan.concept_title}
        Description: {plan.original_concept.concept.description}
        Tech Stack: {plan.original_concept.concept.tech_stack}
        
        File Task Description: {task.description}
        
        Output ONLY the raw file content. No markdown blocks (unless it's a markdown file).
        """
        
        # We use text completion here because we want raw code, not JSON
        content = await api_client.get_text_completion(system_prompt, "Generate the file content.")
        
        # Cleanup potential markdown fences if model adds them
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines)
            
        return content

    async def build_asset(self, plan: BuildPlan) -> Path:
        """
        Executes the build plan, creating directories and files.
        Returns the path to the created asset folder.
        """
        # Create unique folder name
        safe_title = "".join([c for c in plan.concept_title if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        safe_title = safe_title.replace(' ', '_').lower()
        
        asset_path = ASSETS_DIR / safe_title
        asset_path.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"Starting build in: {asset_path}")
        
        for task in plan.files:
            try:
                content = await self.generate_file_content(task, plan)
                file_path = asset_path / task.filename
                
                # Ensure subdirectories exist if filename contains paths
                file_path.parent.mkdir(exist_ok=True, parents=True)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                logger.info(f"Created {task.filename}")
            
            except Exception as e:
                logger.error(f"Failed to build {task.filename}: {e}")
                # We continue building other files even if one fails
        
        logger.info(f"Build complete for: {plan.concept_title}")
        return asset_path
