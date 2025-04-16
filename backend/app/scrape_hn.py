from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from selenium.common.exceptions import WebDriverException
from typing import List, Dict, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service('C:\\Users\\Kuroky\\Documents\\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

BASE_URL = "https://news.ycombinator.com/"


def scrape_hn() -> List[Dict[str, Optional[str]]]:
    try:
        driver.get(BASE_URL)
        headlines = []
        max_retries = 3

        for page in range(5):
            retries = 0
            while retries < max_retries:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((
                            By.CLASS_NAME, 'athing'))
                    )

                    stories = driver.find_elements(By.CLASS_NAME, 'athing')

                    for story in stories:
                        try:
                            title_element = story.find_element(
                                By.CSS_SELECTOR, '.titleline > a')
                            title = title_element.text
                            url = title_element.get_attribute('href')

                            try:
                                score_element = story.find_element(
                                    By.XPATH, "following-sibling::tr")\
                                    .find_element(By.CLASS_NAME, 'score')
                                score = int(score_element.text.split()[0])
                            except Exception:
                                score = 0

                            headlines.append({
                                "title": title,
                                "url": url,
                                "score": score
                            })
                            logger.info(
                                f"Extracted headline: {title} Score: {score}")
                        except Exception as e:
                            logger.warning(
                                f"Error extracting story details: {e}")

                    next_button = driver.find_element(By.LINK_TEXT, 'More')
                    next_button.click()
                    logger.info(f"Navigating to page {page + 2}.")
                    time.sleep(2)
                    break
                except WebDriverException as e:
                    retries += 1
                    logger.warning(
                        f"Error processing page {page + 1}, "
                        f"attempt {retries}: {e}"
                    )
                    time.sleep(2)

            if retries == max_retries:
                logger.error(
                    f"Failed to process page {page + 1} after {max_retries} "
                    f"attempts."
                )
                break

        driver.quit()
        return headlines
    except Exception as e:
        logger.error(
            f"General error during Hacker News scraping: {e}"
        )
        driver.quit()
        return []


if __name__ == "__main__":
    results = scrape_hn()
    for result in results:
        print(result)
