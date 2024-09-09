def individual_serial(game) -> dict:
    return {
        "id": game["id"],
        "description": game["description"],
        "name": game["name"],
        "imageId": game["imageId"],
        "variants": game["variants"],
    }


def list_serial(games) -> list:
    return [individual_serial(game) for game in games]
