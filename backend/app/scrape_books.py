import logging
import redis
import requests
from bs4 import BeautifulSoup
import time
import json
from requests.exceptions import RequestException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(
    host='localhost', port=6379, decode_responses=True
)

BASE_URL = "https://books.toscrape.com/catalogue/"


def scrape_books() -> None:
    page = 1
    max_retries = 3

    while True:
        url = f"{BASE_URL}page-{page}.html"
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    logger.warning(
                        f"Pagination ended at page {page}."
                    )
                    return

                soup = BeautifulSoup(response.text, 'html.parser')
                books = soup.find_all('article', class_='product_pod')

                for book in books:
                    title = book.h3.a['title']
                    price = float(book.find(
                        'p', class_='price_color').text[2:])
                    category = book.find(
                        'p', class_='instock availability'
                    ).text.strip()
                    image_url = BASE_URL + book.img['src']

                    if price < 20:
                        book_id = hash(title)
                        book_data = {
                            "title": title,
                            "price": price,
                            "category": category,
                            "image_url": image_url,
                        }
                        redis_client.set(
                            f"book:{book_id}", json.dumps(book_data)
                        )
                        logger.info(f"Book stored: {title} ({price}£)")

                next_page = soup.find('li', class_='next')
                if not next_page:
                    logger.info("No more pages to process.")
                    return

                page += 1
                break
            except RequestException as e:
                retries += 1
                logger.warning(
                    f"""Error processing page {page},
                    attempt {retries}/{max_retries}: {e}"""
                )
                time.sleep(2)

        if retries == max_retries:
            logger.error(
                f"Failed to process page {page} after {max_retries} attempts."
            )
            return


if __name__ == "__main__":
    scrape_books()
