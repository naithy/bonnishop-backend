def individual_serial(item) -> dict:
    return {
        "id": str(item["_id"]),
        "username": item["email"],
        "password": item["password"],
    }
