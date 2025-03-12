import asyncio
import json
import random

from apify import Actor
import google.generativeai as genai
import os

from google.api_core.exceptions import TooManyRequests
from google.generativeai.types import GenerateContentResponse


async def call_gemini_api(actor: Actor, prompt: str, api_key: str = None, model="gemini-2.0-flash-lite", max_tokens=100000) -> json:
    """
    Calls the Google Gemini API to parse a prompt and return a response.

    Args:
        actor (Actor): The initialized Apify Actor instance.
        prompt (str): The input prompt to send to the API.
        api_key (str, optional): Your Gemini API key. If None, uses GOOGLE_API_KEY env variable.
        model (str): The Gemini model to use (e.g., "gemini-2.0-flash-lite"). Check API docs for available models.
        max_tokens (int): Maximum number of tokens in the response.

    Returns:
        json: The API response text, or an error message if the call fails.
    """
    try:
        # Configure the API key
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("API key not provided and GEMINI_API_KEY environment variable not set.")

        genai.configure(api_key=api_key)

        # Initialize the model
        model_instance = genai.GenerativeModel(model)

        # Set generation configuration
        generation_config = {
            "max_output_tokens": max_tokens,
            "temperature": 0.0,
            "top_p": 0.9,
            "response_mime_type": "application/json",
        }

        # Assign random id for parallel processing tracking
        random_id: int = random.randint(100000, 999999)
        actor.log.info(f"Input for - {random_id} is: {prompt}")

        response: GenerateContentResponse
        # Call the API with the prompt
        for attempt in range(8):
            try:
                response = await asyncio.to_thread(
                    model_instance.generate_content,
                    contents=prompt,
                    generation_config=generation_config
                )

                actor.log.info(f"Output for - {random_id} is: {response.text}")

                # Extract and return the response text
                return json.loads(response.text)

            except TooManyRequests:
                wait_time = 2 ** attempt
                actor.log.info(f"Gemini rate limit hit for {random_id}, waiting {wait_time}s...")
                await asyncio.sleep(wait_time)
        raise Exception(f"Max retries exceeded for - {random_id}")

    except Exception as e:
        raise ValueError(f"Error calling Gemini API: {str(e)}")
