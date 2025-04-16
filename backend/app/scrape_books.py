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

BASE_URL = "https://books.toscrape.com/"


def scrape_books() -> None:
    max_retries = 3

    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        cat_links = soup.select('.side_categories ul.nav-list ul li a')
        categories = [
            (cat.text.strip(), BASE_URL + cat['href']) for cat in cat_links
        ]
    except RequestException as e:
        logger.error(f"Error obtaining categories: {e}")
        return

    for cat_name, category_url in categories:
        logger.info(f"Processing category: {cat_name}")
        page = 1

        while True:
            print(f"Scraping {category_url}...")
            retry = 0
            exito = False

            while retry < max_retries and not exito:
                try:
                    response = requests.get(category_url)
                    if response.status_code != 200:
                        logger.warning(
                            f"No more pages in category {cat_name}.")
                        exito = False
                        break

                    soup = BeautifulSoup(response.text, 'html.parser')
                    books = soup.find_all('article', class_='product_pod')

                    for book in books:
                        title = book.h3.a['title']
                        price = float(
                            book.find('p', class_='price_color').text[2:]
                        )
                        image_url = BASE_URL + book.img['src']

                        if price < 20:
                            book_id = hash(title)
                            book_data = {
                                "title": title,
                                "price": price,
                                "category": cat_name,
                                "image_url": image_url,
                            }
                            redis_client.set(
                                f"book:{book_id}", json.dumps(book_data)
                            )
                            logger.info(
                                f"Book stored: {title} ({price}£)"
                            )

                    next_page = soup.find('li', class_='next')
                    exito = True
                    break

                except RequestException as e:
                    retry += 1
                    logger.warning(
                        f"Error processing page {page}"
                        f" of category {cat_name}, "
                        f"attempt {retry}/{max_retries}: {e}"
                    )
                    time.sleep(2)

            if not exito or retry == max_retries:
                logger.error(
                    f"Failed to process page {page} of category {cat_name} "
                    f"after {max_retries} attempts, or no more pages."
                )
                break

            if not next_page:
                logger.info(f"No more pages for category {cat_name}.")
                break

            next_page_url = next_page.a['href']
            category_url = requests.compat.urljoin(category_url, next_page_url)
            page += 1


if __name__ == "__main__":
    scrape_books()
