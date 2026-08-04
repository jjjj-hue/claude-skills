#!/usr/bin/env python3
import argparse
import asyncio

from crawl4ai import AsyncWebCrawler


async def scrape(url: str) -> str:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown


def main():
    parser = argparse.ArgumentParser(description="Scrape a URL and print its markdown output")
    parser.add_argument("url", help="URL to scrape")
    args = parser.parse_args()

    markdown = asyncio.run(scrape(args.url))
    print(markdown)


if __name__ == "__main__":
    main()
