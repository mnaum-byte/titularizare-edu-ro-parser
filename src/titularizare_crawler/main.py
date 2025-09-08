import sys
import time
from typing import Iterable, Set

import requests
from bs4 import BeautifulSoup


BASE_URL: str = "https://titularizare.edu.ro"
USER_AGENT: str = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def fetch_url(url: str, timeout_seconds: int = 20) -> str:
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=timeout_seconds)
    response.raise_for_status()
    return response.text


def extract_links(html: str, base_url: str = BASE_URL) -> Set[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: Set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href: str = anchor["href"].strip()
        if href.startswith("http://") or href.startswith("https://"):
            if href.startswith(base_url):
                links.add(href)
        elif href.startswith("/"):
            links.add(base_url.rstrip("/") + href)
    return links


def crawl(start_urls: Iterable[str], max_pages: int = 20, delay_seconds: float = 0.5) -> None:
    visited: Set[str] = set()
    to_visit: list[str] = [*start_urls]
    pages_crawled: int = 0

    while to_visit and pages_crawled < max_pages:
        url: str = to_visit.pop(0)
        if url in visited:
            continue
        try:
            html = fetch_url(url)
        except Exception as exc:  # noqa: BLE001
            print(f"Failed to fetch {url}: {exc}")
            visited.add(url)
            continue

        print(f"Fetched: {url}")
        visited.add(url)
        pages_crawled += 1

        for link in extract_links(html):
            if link not in visited and link not in to_visit:
                to_visit.append(link)

        time.sleep(delay_seconds)


def main() -> None:
    # If launched as a module, run the web app instead of crawler
    try:
        from .webapp import create_app

        app = create_app()

        # Enable debug reloader for live code reloads during development
        app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=True)
    except Exception:
        # Fallback: run crawler demo
        start = [BASE_URL]
        crawl(start_urls=start, max_pages=10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)


