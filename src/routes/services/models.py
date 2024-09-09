def individual_serial(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "image": item["image"],
        "description": item["description"],
        "account": item["account"],
        "subscription": item["subscription"],
        "replenishment_balance": item["replenishmentBalance"],
        "change_region": item["changeRegion"],
        "gift_card": item["giftCard"],
        "donate": item["donate"],
        "boost": item["boost"],
        "battle_pass": item["battlePass"],
    }


def list_serial(items) -> list:
    return [individual_serial(item) for item in items]
