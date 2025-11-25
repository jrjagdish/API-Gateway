import httpx
from app.core.config import settings


API_KEY = settings.TOMORROW_API_KEY

async def fetch_weather(city: str):
    cache_key = f"weather:{city}"

    
   
    
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={API_KEY}"

    async with httpx.AsyncClient() as client:
        res = await client.get(url)

    if res.status_code != 200:
        return None

    data = res.json()
  

    return {
        "city": city,
        "temperature": data["data"]["values"]["temperature"],
        "humidity": data["data"]["values"]["humidity"],
        "windSpeed": data["data"]["values"]["windSpeed"],
        "condition": data["data"]["values"]["weatherCode"],
    }
