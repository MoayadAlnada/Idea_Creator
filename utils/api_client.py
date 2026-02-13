import os
from openai import AsyncOpenAI
import httpx
from config import OPENAI_API_KEY, MODEL_NAME, FAST_MODEL_NAME
from utils.logger import setup_logger
from utils.resiliency import async_retry

logger = setup_logger("api_client")

if not OPENAI_API_KEY:
    logger.critical("OPENAI_API_KEY is not set! The system will fail.")

class APIClient:
    def __init__(self):
        # Prevent crash if key is missing (for AI-disabled mode)
        # AsyncOpenAI requires a non-empty key even if not used.
        key = OPENAI_API_KEY if OPENAI_API_KEY else "dummy-key-for-ai-off-mode"
        
        self.client = AsyncOpenAI(
            api_key=key,
            http_client=httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=5, max_connections=10))
        )
    
    @async_retry(max_attempts=3)
    async def get_json_completion(self, system_prompt: str, user_prompt: str, model: str = MODEL_NAME) -> str:
        """
        Request a JSON response from OpenAI.
        """
        try:
            logger.debug(f"Sending request to {model}...")
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            logger.debug("Received response.")
            return content
        except Exception as e:
            logger.error(f"API Error: {e}")
            raise

    @async_retry(max_attempts=3)
    async def get_text_completion(self, system_prompt: str, user_prompt: str, model: str = MODEL_NAME) -> str:
        """
        Request a standard text response.
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"API Error: {e}")
            raise

# Global instance
api_client = APIClient()
