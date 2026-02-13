import json
from pydantic import BaseModel
from typing import List, Dict
from utils.logger import setup_logger
from utils.api_client import api_client
from core.validator import ValidatedConcept

logger = setup_logger("planner")

class FileTask(BaseModel):
    filename: str
    description: str
    dependencies: List[str]

class BuildPlan(BaseModel):
    concept_title: str
    files: List[FileTask]
    original_concept: ValidatedConcept

class Planner:
    def __init__(self):
        pass

    async def create_plan(self, validated_concept: ValidatedConcept) -> BuildPlan:
        """
        Creates a detailed file-by-file build plan.
        """
        concept = validated_concept.concept
        logger.info(f"Planning build for: {concept.title}")
        
        system_prompt = """
        You are a Senior Software Architect.
        Break down the given 'Digital Asset Concept' into a list of files needed to build it.
        Keep it simple (MVP).
        
        Mandatory Files:
        - README.md (Detailed usage instructions)
        - Main logic file (e.g. main.py, script.js)
        - requirements.txt / package.json (if needed)
        - configuration (if needed)

        Output JSON:
        {
            "files": [
                {"filename": "README.md", "description": "...", "dependencies": []},
                {"filename": "main.py", "description": "...", "dependencies": ["requirements.txt"]},
                ...
            ]
        }
        """
        
        user_prompt = f"""
        Concept Title: {concept.title}
        Description: {concept.description}
        Tech Stack: {concept.tech_stack}
        Key Features: {concept.key_features}
        """

        try:
            response_text = await api_client.get_json_completion(system_prompt, user_prompt)
            data = json.loads(response_text)
            
            file_tasks = []
            for item in data['files']:
                file_tasks.append(FileTask(
                    filename=item['filename'],
                    description=item['description'],
                    dependencies=item.get('dependencies', [])
                ))
            
            plan = BuildPlan(
                concept_title=concept.title,
                files=file_tasks,
                original_concept=validated_concept
            )
            
            logger.info(f"Plan created with {len(file_tasks)} files.")
            return plan

        except Exception as e:
            logger.error(f"Planning failed: {e}")
            raise
