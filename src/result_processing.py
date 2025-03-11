import json

from apify import Actor


def process_results(actor: Actor, output: json) -> json:
    result: json = json.loads("{}")

    if output is None: return

    if "id" in output:
        result["url"] = output["url"]
        result["name"] = output["title"]
        result["description"] = output["description"]
        result["location"] = output["location"]
        result["rating"] = __calculate_airbnb_rating(output["rating"])
        result["numberOfRatings"] = output["rating"]["reviewsCount"]
        result["price"] = output["price"]["price"]
    elif "hotelId" in output:
        result["url"] = output["url"]
        result["name"] = output["name"]
        result["description"] = output["description"]
        result["location"] = output["address"]["full"]
        result["rating"] = output["rating"]
        result["numberOfRatings"] = output["reviews"]
        result["price"] = output["price"]
    else:
        actor.log(f"Schema type not found for: {str(output)}")
        return

    return result


def __calculate_airbnb_rating(rating: json) -> float:
    gross_rating: float = 0.0
    number_of_rating_parameters: int = 0

    try:
        gross_rating += rating["accuracy"]
        number_of_rating_parameters += 1
    except KeyError: pass

    try:
        gross_rating += rating["checking"]
        number_of_rating_parameters += 1
    except KeyError: pass

    try:
        gross_rating += rating["cleanliness"]
        number_of_rating_parameters += 1
    except KeyError: pass

    try:
        gross_rating += rating["communication"]
        number_of_rating_parameters += 1
    except KeyError: pass

    try:
        gross_rating += rating["location"]
        number_of_rating_parameters += 1
    except KeyError: pass

    try:
        gross_rating += rating["value"]
        number_of_rating_parameters += 1
    except KeyError: pass

    try:
        gross_rating += rating["guestSatisfaction"]
        number_of_rating_parameters += 1
    except KeyError: pass

    if number_of_rating_parameters == 0: return 0.0
    else: return gross_rating / number_of_rating_parameters
