import json
import os
import asyncio

from apify import Actor

from src.apify_requests import get_airbnb_output, get_booking_output
from src.templates.builder import get_output_prompt, get_input_prompt
from src.gemini import call_gemini_api
from src.result_processing import process_results


async def main() -> None:
    async with (Actor):
        input_data = await Actor.get_input() or {}
        input_filter = input_data.get("filter") or "Looking for a 2-bedroom accommodation in Barcelona with ratings above 4.0 and a price between $100 and $300 per night"
        advanced_filter = input_data.get("advancedFilter") or "I want the property to have a beautiful sea-side view. I also want to only see discounted properties with air conditioning and a private kitchen."
        scraping_limit = input_data.get("scrapingLimit") or 4
        match_exact_filter = input_data.get("matchExactFilter") or True

        __log_actor_input(input_filter, advanced_filter, scraping_limit, match_exact_filter)

        input_analysis_prompt: str = get_input_prompt (
            "src/templates/input_prompt", input_filter, match_exact_filter
        )
        input_response: json = await call_gemini_api(Actor, input_analysis_prompt, os.getenv("GEMINI_API_KEY"))

        if isinstance(input_response, list): input_response = input_response[0]

        Actor.log.info("The input is: " + str(input_response))

        if input_response["error"] != "":
            await Actor.fail(status_message=input_response["error"])

        booking_output, airbnb_output = await asyncio.gather (
            get_booking_output(input_response, scraping_limit),
            get_airbnb_output(input_response, scraping_limit)
        )

        if advanced_filter is not None and advanced_filter.strip() != "":
            output_prompt: str = get_output_prompt (
                "src/templates/output_prompt", advanced_filter, match_exact_filter
            )

            tasks = [__apply_output_filter(output, output_prompt) for output in booking_output] + \
                    [__apply_output_filter(output, output_prompt) for output in airbnb_output]

            results = await asyncio.gather(*tasks)

            for result in results:
                await Actor.push_data(process_results(Actor, result))

            await Actor.exit()

        for booking in booking_output:
            await Actor.push_data(process_results(Actor, booking))
            await Actor.charge("simple-filtering-charge", 1)

        for airbnb in airbnb_output:
            await Actor.push_data(process_results(Actor, airbnb))
            await Actor.charge("simple-filtering-charge", 1)


def __log_actor_input(input_filter: str, advanced_filter: str, scraping_limit: int, match_exact_filter: bool) -> None:
    Actor.log.info("The input filter is: " + input_filter)
    Actor.log.info("The advanced filter is: " + advanced_filter)
    Actor.log.info("The scraping limit is: " + str(scraping_limit))
    Actor.log.info("The exact filter matching parameter is: " + str(match_exact_filter))


async def __apply_output_filter(output: json, output_prompt: str) -> json:
    prompt = output_prompt.replace("REPLACE_THIS_INPUT", json.dumps(output))

    output_response: json = await call_gemini_api(Actor, prompt, os.getenv("GEMINI_API_KEY"))

    # Handle responses that come out as lists
    if isinstance(output_response, list): output_response = output_response[0]

    if output_response["matchesFilter"]: return output
