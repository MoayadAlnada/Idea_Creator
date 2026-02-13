import json
from typing import List, Optional
from pydantic import BaseModel
from utils.logger import setup_logger
from utils.api_client import api_client
from core.scanner import Trend

logger = setup_logger("analyzer")

class OpportunityScore(BaseModel):
    trend_title: str
    demand_score: int # 0-100
    competition_score: int # 0-100 (Lower is better usually, but we'll normalize)
    buildability_score: int # 0-100
    total_score: int
    reasoning: str
    suggested_asset_type: str # e.g., "Python Script", "Template", "React Component"

class Analyzer:
    def __init__(self):
        pass

    async def analyze_trend(self, trend: Trend) -> Optional[OpportunityScore]:
        """
        Analyzes a single trend and returns a score.
        """
        system_prompt = """
        You are an expert market analyst for digital assets (code, templates, tools).
        Analyze the given tech trend.
        Determine if there is a viable 'Digital Asset' or 'Micro-SaaS' opportunity.
        
        Scoring Criteria:
        - Demand: Is this a hot topic? Are people looking for solutions? (0-100)
        - Competition: Is it overcrowded? (0=Overcrowded, 100=Blue Ocean)
        - Buildability: Can a single developer build a useful asset in < 2 days? (0-100)
        
        Output JSON only:
        {
            "demand": int,
            "competition": int,
            "buildability": int,
            "reasoning": "string",
            "suggested_asset": "string (e.g. 'Automation Script')"
        }
        """
        
        user_prompt = f"""
        Trend: {trend.title}
        Source: {trend.source}
        Summary: {trend.summary}
        """

        try:
            response_text = await api_client.get_json_completion(system_prompt, user_prompt)
            data = json.loads(response_text)
            
            # Simple weighted average
            total = (data['demand'] * 0.4) + (data['competition'] * 0.3) + (data['buildability'] * 0.3)
            
            score = OpportunityScore(
                trend_title=trend.title,
                demand_score=data['demand'],
                competition_score=data['competition'],
                buildability_score=data['buildability'],
                total_score=int(total),
                reasoning=data['reasoning'],
                suggested_asset_type=data['suggested_asset']
            )
            
            logger.info(f"Analyzed '{trend.title[:30]}...': Score {score.total_score}")
            return score

        except Exception as e:
            logger.error(f"Analysis failed for {trend.title}: {e}")
            return None

    async def analyze_batch(self, trends: List[Trend]) -> List[OpportunityScore]:
        """
        Analyzes a batch of trends.
        """
        logger.info(f"Analyzing batch of {len(trends)} trends...")
        results = []
        for trend in trends:
            # For MVP, sequential to avoid rate limits provided by user key limits.
            # In full prod, we'd use asemaphore.
            score = await self.analyze_trend(trend)
            if score and score.total_score > 60: # Threshold
                results.append(score)
        
        results.sort(key=lambda x: x.total_score, reverse=True)
        return results
