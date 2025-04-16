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
    title: Optional[str] = Field(None, max_length=100, description="Título del libro a buscar")
    category: Optional[str] = Field(None, max_length=50, description="Categoría del libro a buscar")

class InitResponse(BaseModel):
    message: str = Field(..., description="Mensaje indicando el estado del scraping de libros.")

app = FastAPI()

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.post("/init", response_model=InitResponse, summary="Inicia el scraping de libros", description="Este endpoint inicia el proceso de scraping de libros desde Books to Scrape y almacena los datos en Redis.")
def init_scraping() -> InitResponse:
    try:
        logger.info("Iniciando el scraping de libros.")
        scrape_books()
        logger.info("Scraping de libros completado.")
        return {"message": "Scraping de libros completado."}
    except Exception as e:
        logger.error(f"Error en el endpoint /init: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books/search", response_model=List[Dict[str, Any]], summary="Busca libros por título o categoría", description="Este endpoint permite buscar libros almacenados en Redis filtrando por título o categoría.")
def search_books(query: BookQuery) -> List[Dict[str, Any]]:
    try:
        logger.info(f"Buscando libros con los parámetros: {query.dict()}.")
        keys = redis_client.keys("book:*")
        books = [json.loads(redis_client.get(key)) for key in keys]
        print(books)

        if query.title:
            books = [book for book in books if query.title.lower() in book["title"].lower()]
        if query.category:
            books = [book for book in books if query.category.lower() in book["category"].lower()]

        logger.info(f"Se encontraron {len(books)} libros que coinciden con los parámetros.")
        return books
    except Exception as e:
        logger.error(f"Error en el endpoint /books/search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/headlines", response_model=List[Dict[str, Any]], summary="Obtiene titulares de Hacker News", description="Este endpoint obtiene titulares de Hacker News en tiempo real, incluyendo título, URL y puntuación.")
def get_headlines() -> List[Dict[str, Any]]:
    try:
        logger.info("Iniciando la obtención de titulares de Hacker News.")
        headlines = scrape_hn()
        logger.info(f"Se obtuvieron {len(headlines)} titulares de Hacker News.")
        return headlines
    except Exception as e:
        logger.error(f"Error en el endpoint /headlines: {e}")
        raise HTTPException(status_code=500, detail=str(e))
