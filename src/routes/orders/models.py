def individual_serial(game) -> dict:
    return {
        "id": str(game["_id"]),
        "payment_id": game["payment_id"],
        "shop": game["shop"],
        "amount": game["amount"],
        "profit": game["profit"],
        "desc": game["desc"],
        "currency": game["currency"],
        "currency_amount": game["currency_amount"],
        "sign": game["sign"],
        "email": game["email"],
        "date": game["date"],
        "method": game["method"],
        "custom": game["custom"],
        "underpayment": game["underpayment"],
    }


def list_serial(games) -> list:
    return [individual_serial(game) for game in games]