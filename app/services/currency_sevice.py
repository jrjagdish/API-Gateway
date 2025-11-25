import httpx
from app.core.config import settings



BASE_URL = "https://api.freecurrencyapi.com/v1/latest"


async def convert_currency(from_currency: str, to_currency: str, amount: float = 1):
    cache_key = f"currency:{from_currency}:{to_currency}"

  

    params = {
        "apikey": settings.FREECURRENCY_API_KEY,
        "base_currency": from_currency.upper()
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(BASE_URL, params=params)
            data = response.json()

       
        if "data" not in data:
            return None

        rates = data["data"]

        if to_currency.upper() not in rates:
            return None

        rate = rates[to_currency.upper()]
        converted = rate * amount
        

        return {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "rate": rate,
            "amount": amount,
            "converted_value": converted
        }

    except Exception as e:
        print("Currency API error:", e)
        return None
