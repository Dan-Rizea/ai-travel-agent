import json

from apify import Actor
import google.generativeai as genai
import os


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

        # Charge input tokens from user
        input_tokens = model_instance.count_tokens(prompt).total_tokens
        await __charge_user_per_token(actor, input_tokens, "output")

        # Call the API with the prompt
        response = model_instance.generate_content (
            contents=prompt,
            generation_config=generation_config
        )

        # Charge output tokens from user - they are 4x more expensive than input tokens
        output_tokens = model_instance.count_tokens(response.text).total_tokens * 4
        await __charge_user_per_token(actor, output_tokens, "output")

        # Extract and return the response text
        return json.loads(response.text)

    except Exception as e:
        raise ValueError(f"Error calling Gemini API: {str(e)}")


async def __charge_user_per_token(actor: Actor, tokens: int, token_type: str) -> None:
    """
    Monetization Formula:
    The Apify platform charges 80% of your total revenue.
    (x + x * 1.25) = total cost for Gemini tokens
    (x + x * 1.25) * 1.5 = total cost for Gemini tokens * personal revenue

    Args:
    actor (Actor): The initialized Apify Actor instance.
    tokens (int): The number of tokens as calculated by Gemini SDK
    """
    events_to_charge = (tokens + tokens * 1.25) * 1.5
    Actor.log.info(f"Call to Gemini API - consumed {events_to_charge} {token_type} event tokens")
    await actor.charge('token-charge', events_to_charge)
