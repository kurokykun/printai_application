from fastapi import FastAPI, HTTPException
import redis
from .scrape_books import scrape_books
from .scrape_hn import scrape_hn
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BookQuery(BaseModel):
    title: Optional[str] = Field(None, max_length=100, description="Title of the book to search for")
    category: Optional[str] = Field(None, max_length=50, description="Category of the book to search for")

class InitResponse(BaseModel):
    message: str = Field(..., description="Message indicating the status of the book scraping.")

app = FastAPI()

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.post("/init", response_model=InitResponse, summary="Starts book scraping", description="This endpoint starts the book scraping process from Books to Scrape and stores the data in Redis.")
def init_scraping() -> InitResponse:
    try:
        logger.info("Starting book scraping.")
        scrape_books()
        logger.info("Book scraping completed.")
        return {"message": "Book scraping completed."}
    except Exception as e:
        logger.error(f"Error in the /init endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/books/search", response_model=List[Dict[str, Any]], summary="Search books by title or category", description="This endpoint allows searching for books stored in Redis by filtering by title or category.")
def search_books(query: BookQuery) -> List[Dict[str, Any]]:
    try:
        logger.info(f"Searching for books with parameters: {query.dict()}.")
        keys = redis_client.keys("book:*")
        books = [json.loads(redis_client.get(key)) for key in keys]
        print(books)

        if query.title:
            books = [book for book in books if query.title.lower() in book["title"].lower()]
        if query.category:
            books = [book for book in books if query.category.lower() in book["category"].lower()]

        logger.info(f"Found {len(books)} books matching the parameters.")
        return books
    except Exception as e:
        logger.error(f"Error in the /books/search endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books", response_model=List[Dict[str, Any]], summary="Retrieve books", description="This endpoint retrieves books from Redis, optionally filtering by category.")
def get_books(category: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        logger.info(f"Retrieving books with category filter: {category}.")
        keys = redis_client.keys("book:*")
        books = [json.loads(redis_client.get(key)) for key in keys]

        if category:
            books = [book for book in books if category.lower() in book["category"].lower()]

        logger.info(f"Retrieved {len(books)} books.")
        return books
    except Exception as e:
        logger.error(f"Error in the /books endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/headlines", response_model=List[Dict[str, Any]], summary="Fetch Hacker News headlines", description="This endpoint fetches real-time Hacker News headlines, including title, URL, and score.")
def get_headlines() -> List[Dict[str, Any]]:
    try:
        logger.info("Starting to fetch Hacker News headlines.")
        headlines = scrape_hn()
        logger.info(f"Fetched {len(headlines)} Hacker News headlines.")
        return headlines
    except Exception as e:
        logger.error(f"Error in the /headlines endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
