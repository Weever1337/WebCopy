import argparse
import asyncio
from urllib.parse import urlparse
from src.webcopy import download_page
from src import logger

async def main():
    parser = argparse.ArgumentParser(description="Webcopy")
    parser.add_argument(
        "-u", "-l", "--url", "--link", type=str, help="The URL of the website to copy"
    )
    parser.add_argument(
        "-d", "-debug", "--debug", action="store_true", help="Enable debug mode"
    )
    args = parser.parse_args()
    url = args.url or input("Enter the URL of the website: ")
    debug = args.debug or False
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    folder_name = "copied/" + urlparse(url).netloc
    logger.info(f"Downloading website from {url} to {folder_name}")
    await download_page(url, folder_name, debug)


if __name__ == "__main__":
    asyncio.run(main())
