import httpx
from app.core.config import settings


BASE_URL = "https://newsdata.io/api/1/news"
API_KEY = settings.NEWS_API_KEY

async def fetch_news(query: str, language: str = "en"):
    cache_key = f"news:{query}"

  
   
    params = {
        "apikey": API_KEY,
        "q": query,
        "language": language
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    articles = []
    for item in data.get("results", []):
        articles.append({
            "title": item.get("title"),
            "description": item.get("description"),
            "url": item.get("link"),
            "source": item.get("source_id"),
            "published_at": item.get("pubDate")
        })

    return {
        "total": len(articles),
        "articles": articles
    }