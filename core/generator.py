import json
from pydantic import BaseModel
from typing import List, Optional
from utils.logger import setup_logger
from utils.api_client import api_client
from core.analyzer import OpportunityScore

logger = setup_logger("generator")

class AssetConcept(BaseModel):
    title: str
    description: str
    target_audience: str
    key_features: List[str]
    tech_stack: List[str]
    monetization_angle: str
    original_opportunity: OpportunityScore

class Generator:
    def __init__(self):
        pass

    async def generate_concept(self, opportunity: OpportunityScore) -> Optional[AssetConcept]:
        """
        Generates a concrete asset concept from a scored opportunity.
        """
        logger.info(f"Generating concept for: {opportunity.trend_title}")
        
        system_prompt = """
        You are a product innovator. Convert the given 'Opportunity' into a concrete 'Digital Asset Concept'.
        The asset must be buildable by a single developer in < 2 days.
        Focus on "Micro-SaaS", "Automation Script", or "High-Value Template".
        
        Output JSON:
        {
            "title": "Configurable Title",
            "description": "Short pitch",
            "target_audience": "Who buys this?",
            "key_features": ["feature1", "feature2", "feature3"],
            "tech_stack": ["python", "react", etc],
            "monetization_angle": "How to sell/distribute (e.g. Gumroad $5, Open Source Lead Magnet)"
        }
        """
        
        user_prompt = f"""
        Trend: {opportunity.trend_title}
        Reasoning: {opportunity.reasoning}
        Suggested Type: {opportunity.suggested_asset_type}
        """

        try:
            response_text = await api_client.get_json_completion(system_prompt, user_prompt)
            data = json.loads(response_text)
            
            concept = AssetConcept(
                title=data['title'],
                description=data['description'],
                target_audience=data['target_audience'],
                key_features=data['key_features'],
                tech_stack=data['tech_stack'],
                monetization_angle=data['monetization_angle'],
                original_opportunity=opportunity
            )
            
            logger.info(f"Generated Concept: {concept.title}")
            return concept
            
        except Exception as e:
            logger.error(f"Generation failed for {opportunity.trend_title}: {e}")
            return None
