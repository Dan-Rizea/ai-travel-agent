import json
import os
from apify_client import ApifyClient

from src.templates.builder import get_mock_output


async def get_booking_output(input_response: json, scraping_limit: int) -> json:
    booking_input: json = input_response["bookingdotcom"]

    # CHANGE TO USER INPUT IN PROD
    booking_input["maxItems"] = scraping_limit

    if booking_input["propertyType"] is None: del booking_input["propertyType"]
    if booking_input["starsCountFilter"] is None: del booking_input["starsCountFilter"]
    if booking_input["currency"] is None: del booking_input["currency"]
    if booking_input["rooms"] is None: del booking_input["rooms"]
    if booking_input["adults"] is None: del booking_input["adults"]
    if booking_input["children"] is None: del booking_input["children"]
    if booking_input["minMaxPrice"] is None: del booking_input["minMaxPrice"]

    output = await __send_apify_request('oeiQgfg5fsmIJB7Cn', booking_input, scraping_limit)
    # output = get_mock_output("src/templates/bookingdotcom_mock")

    for entry in output:
        print(str(entry))
        del entry["location"]
        del entry["image"]
        del entry["images"]
        del entry["roomImages"]
        del entry["breadcrumbs"]

    return output


async def get_airbnb_output(input_response: json, scraping_limit: int) -> json:
    airbnb_input = input_response["airbnb"]

    if airbnb_input["adults"] is None: del airbnb_input["adults"]
    if airbnb_input["checkIn"] is None: del airbnb_input["checkIn"]
    if airbnb_input["checkOut"] is None: del airbnb_input["checkOut"]
    if airbnb_input["children"] is None: del airbnb_input["children"]
    if airbnb_input["currency"] is None: del airbnb_input["currency"]
    if airbnb_input["infants"] is None: del airbnb_input["infants"]
    if airbnb_input["locale"] is None: del airbnb_input["locale"]
    if airbnb_input["minBathrooms"] is None: del airbnb_input["minBathrooms"]
    if airbnb_input["minBedrooms"] is None: del airbnb_input["minBedrooms"]
    if airbnb_input["minBeds"] is None: del airbnb_input["minBeds"]
    if airbnb_input["pets"] is None: del airbnb_input["pets"]
    if airbnb_input["priceMax"] is None: del airbnb_input["priceMax"]
    if airbnb_input["priceMin"] is None: del airbnb_input["priceMin"]

    output = await __send_apify_request('GsNzxEKzE2vQ5d9HN', airbnb_input, scraping_limit)
    # output = get_mock_output("src/templates/airbnb_mock")

    for entry in output:
        del entry["coordinates"]
        del entry["thumbnail"]
        del entry["androidLink"]
        del entry["iosLink"]
        del entry["breadcrumbs"]
        del entry["htmlDescription"]
        del entry["images"]

    return output


async def __send_apify_request(actor_id: str, actor_input: json, scraping_limit: int) -> json:
    # Initialize the ApifyClient with your API token
    client = ApifyClient(os.getenv('APIFY_TOKEN'))

    # Run the Actor and wait for it to finish
    run = client.actor(actor_id).call(run_input=actor_input, max_items=scraping_limit)

    # Fetch and print Actor results from the run's dataset (if there are any)
    created_dataset = client.dataset(run["defaultDatasetId"]).list_items()

    # Transpose response into json
    json_response = json.loads(json.dumps(created_dataset.items))

    return json_response
