import asyncio
import sys
from config import LOGS_DIR
from utils.logger import setup_logger
from core.ecosystem import Ecosystem

# Setup main logger
logger = setup_logger("main")

async def main():
    logger.info("Antigravity Ecosystem Starting...")
    
    try:
        ecosystem = Ecosystem()
        await ecosystem.start()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
    except Exception as e:
        logger.critical(f"Fatal Error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("System Shutdown Complete.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
