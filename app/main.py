import os
import requests
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

API_VERSION_1 = "api/v1"
CONTROLLER = "news"
TAG = "News"

load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

app = FastAPI(openapi_url="/swagger/v1/swagger.json", openapi_tags=[{"name": f"{TAG}"}],
              docs_url="/swagger/index.html", redoc_url=None)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    return get_openapi(
        version="v1",
        title=f"Global Eye API",
        description="An API to serve React Application [Global Eye](https://jacob-dolorzo-global-eye.vercel.app).",
        contact={
            "name": "Jacob Dolorzo",
            "url": "https://jacob-dolorzo.vercel.app",
            "email": "jacob.dolorzo.96@gmail.com",
        },
        routes=app.routes,
    )


app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fetch_from_news_api(url: str):
    response = requests.get(url)
    return response.json()


@app.get(f"/{API_VERSION_1}/{CONTROLLER}/fetch-all-news({{selected_searched_source}})", tags=[f"{TAG}"])
async def fetch_news(selected_searched_source: str):
    news_url = f"https://newsapi.org/v2/everything?{selected_searched_source}&apiKey={NEWS_API_KEY}"
    return fetch_from_news_api(news_url)
