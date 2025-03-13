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
        gemini_api_key = input_data.get("geminiApiKey") or os.getenv("GEMINI_API_KEY")
        input_filter = input_data.get("filter") or "Looking for a 2-bedroom accommodation in Barcelona with ratings above 4.0 and a price between $100 and $300 per night"
        advanced_filter = input_data.get("advancedFilter") or "I want the property to have a beautiful sea-side view. I also want to only see discounted properties with air conditioning and a private kitchen."
        booking_scraping_limit = input_data.get("bookingScrapingLimit") or 3
        airbnb_scraping_limit = input_data.get("airbnbScrapingLimit") or 3
        match_exact_filter = input_data.get("matchExactFilter") or False

        __log_actor_input(input_filter, advanced_filter, booking_scraping_limit, airbnb_scraping_limit, match_exact_filter)

        input_analysis_prompt: str = get_input_prompt (
            "src/templates/input_prompt", input_filter, match_exact_filter
        )
        input_response: json = await call_gemini_api(Actor, input_analysis_prompt, gemini_api_key)

        if isinstance(input_response, list): input_response = input_response[0]

        Actor.log.info("The input is: " + str(input_response))

        if input_response["error"] != "":
            await Actor.fail(status_message=input_response["error"])

        booking_output, airbnb_output = await asyncio.gather (
            get_booking_output(input_response, booking_scraping_limit),
            get_airbnb_output(input_response, airbnb_scraping_limit)
        )

        if advanced_filter is not None and advanced_filter.strip() != "":
            output_prompt: str = get_output_prompt (
                "src/templates/output_prompt", advanced_filter, match_exact_filter
            )

            tasks = [
                __apply_advanced_filtering(Actor, gemini_api_key, output, output_prompt)
                for output in booking_output + airbnb_output
            ]

            results = await asyncio.gather(*tasks)

            await Actor.charge("scraped-input-charge", booking_scraping_limit + airbnb_scraping_limit)

            for result in results:
                if result: await Actor.push_data(process_results(Actor, result))

            await Actor.exit()

        await Actor.charge("scraped-input-charge", booking_scraping_limit or 0 + airbnb_scraping_limit or 0)

        for booking in booking_output:
            await Actor.push_data(process_results(Actor, booking))

        for airbnb in airbnb_output:
            await Actor.push_data(process_results(Actor, airbnb))


def __log_actor_input(input_filter: str, advanced_filter: str, booking_scraping_limit: int,
                      airbnb_scraping_limit: int, match_exact_filter: bool) -> None:
    Actor.log.info("The input filter is: " + input_filter)
    Actor.log.info("The advanced filter is: " + advanced_filter)
    Actor.log.info("The booking scraping limit is: " + str(booking_scraping_limit))
    Actor.log.info("The airbnb scraping limit is: " + str(airbnb_scraping_limit))
    Actor.log.info("The exact filter matching parameter is: " + str(match_exact_filter))


async def __apply_advanced_filtering(actor: Actor, gemini_api_key: str, output: json, output_prompt: str) -> json:
    try:
        output_copy = json.loads(json.dumps(output))
        prompt = output_prompt.replace("REPLACE_THIS_INPUT", json.dumps(output_copy, ensure_ascii=False))

        output_response: json = await call_gemini_api(actor, prompt, gemini_api_key)

        # Handle responses that come out as lists
        if isinstance(output_response, list): output_response = output_response[0]

        # Validate response structure
        if not isinstance(output_response, dict) or "matchesFilter" not in output_response:
            actor.log.error(f"Invalid filter response format: {output_response}")
            return None

        if output_response["matchesFilter"]: return output

    except json.JSONDecodeError as e:
        actor.log.error(f"Failed to serialize output for filtering: {str(e)}")
        return None
    except KeyError as e:
        actor.log.error(f"Missing key in filter response: {str(e)}")
        return None
    except Exception as e:
        actor.log.error(f"Filtering failed: {str(e)}")
        return None
