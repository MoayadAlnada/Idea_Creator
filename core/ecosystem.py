import asyncio
from utils.logger import setup_logger
from core.scanner import Scanner
from core.analyzer import Analyzer
from core.generator import Generator
from core.validator import Validator
from core.planner import Planner
from core.builder import Builder
from core.qa import QA
from core.packager import Packager
from core.publisher import Publisher

logger = setup_logger("ecosystem")

class Ecosystem:
    def __init__(self):
        self.running = False
        self.scanner = Scanner()
        self.analyzer = Analyzer()
        self.generator = Generator()
        self.validator = Validator()
        self.planner = Planner()
        self.builder = Builder()
        self.qa = QA()
        self.packager = Packager()
        self.publisher = Publisher()

    async def start(self):
        """
        Starts the main event loop.
        """
        self.running = True
        logger.info("Ecosystem Engine initialized. Starting loops...")
        
        # Run one full cycle for MVP demonstration
        await self.run_cycle()

    async def run_cycle(self):
        """
        Runs a single end-to-end cycle.
        """
        logger.info(">>> STARTING CYCLE <<<")
        
        # 1. SCAN
        trends = await self.scanner.scan()
        if not trends:
            logger.warning("No trends found. Sleeping.")
            return

        # 2. ANALYZE
        opportunities = await self.analyzer.analyze_batch(trends)
        if not opportunities:
            logger.warning("No viable opportunities found.")
            return
        
        best_opportunity = opportunities[0]
        logger.info(f"Winner Opportunity: {best_opportunity.trend_title} (Score: {best_opportunity.total_score})")

        # 3. GENERATE
        concept = await self.generator.generate_concept(best_opportunity)
        if not concept:
            return

        # 4. VALIDATE
        validated = await self.validator.validate(concept)
        if not validated.is_approved:
            logger.warning(f"Concept rejected by Validator: {validated.validation_notes}")
            return
        
        logger.info(f"Concept Validated! Logic: {validated.validation_notes}")

        # 5. PLAN
        plan = await self.planner.create_plan(validated)
        
        # 6. BUILD
        asset_path = await self.builder.build_asset(plan)
        
        # 7. QA
        qa_result = await self.qa.test_asset(asset_path)
        if not qa_result.passed:
            logger.error(f"QA Failed for {asset_path}: {qa_result.issues}")
            logger.error("🛑 STRICT QA GATE: ABORTING PUBLISH.")
            return
            
        logger.info("QA Passed. Proceeding to Packaging.")
        
        # 8. PACKAGE
        metadata = {
            "title": concept.title,
            "description": concept.description,
            "version": "1.0.0",
            "qa_status": "passed" if qa_result.passed else "failed",
            "tech_stack": concept.tech_stack
        }
        await self.packager.package_asset(asset_path, metadata)
        
        # 9. PUBLISH (Real Mode)
        try:
            from config import STRICT_PUBLISH_MODE, MISSING_KEYS
            logger.info(f"Attempting Publish (Strict Mode: {STRICT_PUBLISH_MODE})")
            repo_url, store_link = await self.publisher.publish(asset_path, metadata)
            logger.info(f"Published: GitHub={repo_url}, Store={store_link}")
        except Exception as e:
            logger.error(f"🛑 PUBLISH ABORTED: {e}")
            logger.error(f"Missing Keys Detected: {MISSING_KEYS if 'MISSING_KEYS' in locals() else 'Check Config'}")
            return

        # 10. MEMORY
        from core.memory import memory
        memory.record_success(f"{concept.title} ({repo_url})")
        
        logger.info(">>> CYCLE COMPLETE - ASSET LIVE <<<")

    async def stop(self):
        self.running = False
