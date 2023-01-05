import logging
from urllib.parse import urljoin
from multiprocessing.dummy import Pool as ThreadPool
import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import argparse

logging.basicConfig(
    format='%(message)s',
    level=logging.INFO)


def fetch_html_content(url: str):
    request = requests.Session()
    retries = Retry(total=2, backoff_factor=1)
    request.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        response = request.get(url, timeout=1)
        return response.text
    except requests.exceptions.HTTPError as errh:
        logging.exception(f"The {url} has Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        logging.exception(f"The {url} has Error Connecting Problem:", errc)
    except requests.exceptions.Timeout as errt:
        logging.exception(f"The {url} has Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        logging.exception(f"The url {url} has Something Else:", err)
    return Non


def get_linked_urls(url: str, html: str):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        path = link.get('href')
        if path and path.startswith('/'):
            path = urljoin(url, path)
        yield path


class Crawler:
    def __init__(self, url: str):
        self.entrypoint = url
        self.visited_urls = set()
        self.urls_queue = [self.entrypoint]

    def validate_url(self, url: str) -> bool:
        return url and url.startswith("http") and url.startswith(self.entrypoint)

    def add_url_to_queue(self, url: str) -> None:
        if url not in self.visited_urls and url not in self.urls_queue and self.validate_url(url):
            self.urls_queue.append(url)

    def crawl(self, url: str) -> None:
        self.visited_urls.add(url)
        html = fetch_html_content(url)
        if html:
            page_content_urls = set()
            for page_url in get_linked_urls(url, html):
                self.add_url_to_queue(page_url)
                page_content_urls.add(page_url)
            urls = [url for url in page_content_urls if url and url.startswith("http")]
            logging.info(f"Current page: {url}\n     The connected url in page: {urls}")

    def run(self) -> None:
        while self.urls_queue:
            pool = ThreadPool(3)
            pool.map(self.crawl, self.urls_queue)
            self.urls_queue.pop(0)
            pool.close()
            pool.join()


def args_helper():
    parser = argparse.ArgumentParser()
    parser.add_argument('entrypoint')
    return parser.parse_args()


if __name__ == '__main__':
    config = args_helper()
    entrypoint = config.entrypoint
    if entrypoint:
        Crawler(entrypoint).run()
