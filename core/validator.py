from pydantic import BaseModel
from utils.logger import setup_logger
from core.generator import AssetConcept
from config import ENABLE_REAL_VALIDATION, SERPER_API_KEY

logger = setup_logger("validator")

class ValidatedConcept(BaseModel):
    concept: AssetConcept
    validation_score: int
    is_approved: bool
    validation_notes: str

class Validator:
    def __init__(self):
        pass

    async def validate(self, concept: AssetConcept) -> ValidatedConcept:
        """
        Validates the concept.
        In MVP, this is logic-based. In Prod, this hits Google Trends/SEO APIs.
        """
        logger.info(f"Validating concept: {concept.title}")
        
        score = 0
        notes = []
        
        # 1. Tech Stack Check (Simple Constraint)
        # We prefer Python/JS for this ecosystem
        preferred_stacks = ["python", "javascript", "typescript", "react", "html", "css", "nodejs"]
        stack_score = 0
        for tech in concept.tech_stack:
            if tech.lower() in preferred_stacks:
                stack_score += 10
        
        # Cap stack score
        score += min(stack_score, 30)
        notes.append(f"Tech Stack Score: {min(stack_score, 30)}")
        
        # 2. Complexity Check (Heuristic)
        # If features > 5, might be too complex for 2 days
        if len(concept.key_features) > 5:
            score -= 20
            notes.append("Penalty: Too many features for MVP.")
        else:
            score += 20
            notes.append("Complexity: Manageable.")

        # 3. Opportunity Score Inheritance
        # We trust the Analyzer's demand score partially
        opp_score = concept.original_opportunity.total_score
        score += int(opp_score * 0.5)
        notes.append(f"Inherited Opportunity Score impact: {int(opp_score * 0.5)}")
        
        # 4. Real External Validation (Serper.dev)
        if ENABLE_REAL_VALIDATION and SERPER_API_KEY:
            try:
                import httpx
                # Check "Demand": Search for the problem/keyword
                # We look at "number of results" as a proxy for competition (lower is better? or high implies market?)
                # Actually, "related queries" or "people also ask" suggests demand.
                # For MVP, we check if there are results (it exists) but not TOO many (blue ocean).
                
                search_term = concept.title
                logger.info(f"Checking Google for: {search_term}")
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "https://google.serper.dev/search",
                        headers={
                            "X-API-KEY": SERPER_API_KEY,
                            "Content-Type": "application/json"
                        },
                        json={"q": search_term, "num": 10}
                    )
                    
                    if response.status_code == 200:
                        results = response.json()
                        organic = results.get("organic", [])
                        
                        # Logic: If we find EXACT matches of our tool name, competition is high?
                        # Or if we find NO results for the problem, maybe no demand?
                        # Let's trust the "Opportunity" score more, and use this to "Verify" it's not a hallucination.
                        
                        if len(organic) > 0:
                            notes.append(f"Google Results Found: {len(organic)}. Validation Passed.")
                            score += 20
                        else:
                            notes.append("No direct Google results. Potential Blue Ocean?")
                            score += 10
                    else:
                        notes.append("Serper API Error. Skipping.")
                        
            except Exception as e:
                logger.error(f"Validation API failed: {e}")
                notes.append("Validation API check failed.")
        else:
             # Simulation: Randomly pass for now, or just assume passed if logic holds
             pass

        final_score = min(max(score, 0), 100)
        is_approved = final_score > 50  # Threshold
        
        logger.info(f"Validation Result: {is_approved} (Score: {final_score})")
        
        return ValidatedConcept(
            concept=concept,
            validation_score=final_score,
            is_approved=is_approved,
            validation_notes=" | ".join(notes)
        )
