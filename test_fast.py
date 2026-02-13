import asyncio
from utils.logger import setup_logger
from core.ecosystem import Ecosystem
from core.scanner import Trend
from core.analyzer import OpportunityScore

logger = setup_logger("test_fast")

async def test_fast_cycle():
    logger.info("Starting FAST Test Cycle...")
    
    ecosystem = Ecosystem()
    
    # Mock Scanner
    logger.info("Mocking Scanner...")
    ecosystem.scanner.scan = asyncio.Future()
    ecosystem.scanner.scan.set_result(None) # Disable real scan
    
    # Create a Fake Opportunity directly
    fake_opp = OpportunityScore(
        trend_title="AI-Powered Markdown Optimizer",
        demand_score=85,
        competition_score=40,
        buildability_score=90,
        total_score=80,
        reasoning="High demand for clean data for LLMs.",
        suggested_asset_type="Python Script"
    )
    
    logger.info(f"Injecting Fake Opportunity: {fake_opp.trend_title}")
    
    # Skip Analyzer processing and go straight to Generator
    # We'll manually invoke the pipeline steps from Analyzer onwards
    
    # 3. GENERATE
    concept = await ecosystem.generator.generate_concept(fake_opp)
    if not concept:
        logger.error("Generation Failed")
        return

    # 4. VALIDATE
    validated = await ecosystem.validator.validate(concept)
    if not validated.is_approved:
        logger.warning(f"Concept rejected: {validated.validation_notes}")
        return
    
    logger.info(f"Concept Validated: {validated.concept.title}")

    # 5. PLAN
    plan = await ecosystem.planner.create_plan(validated)
    
    # 6. BUILD
    asset_path = await ecosystem.builder.build_asset(plan)
    
    # 7. QA
    qa_result = await ecosystem.qa.test_asset(asset_path)
    
    # 8. PACKAGE
    metadata = {
        "title": concept.title,
        "description": concept.description,
        "version": "1.0.0-test",
        "qa_status": "passed" if qa_result.passed else "failed",
        "tech_stack": concept.tech_stack
    }
    await ecosystem.packager.package_asset(asset_path, metadata)
    
    logger.info(f"FAST TEST COMPLETE. Asset at: {asset_path}")

if __name__ == "__main__":
    if asyncio.get_event_loop_policy().__class__.__name__ == 'WindowsProactorEventLoopPolicy':
                 asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_fast_cycle())
