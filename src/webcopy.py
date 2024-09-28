import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from . import logger


async def create_directory_for_resource(resource_url, folder):
    parsed_url = urlparse(resource_url)
    resource_path = parsed_url.path.lstrip("/")
    resource_folder = os.path.join(folder, os.path.dirname(resource_path))

    if not os.path.exists(resource_folder):
        os.makedirs(resource_folder)

    return os.path.join(resource_folder, os.path.basename(resource_path))


async def download_page(url, folder, debug):
    os.makedirs(folder, exist_ok=True)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Error fetching {url}")
                    return

                content = await response.text()
                with open(
                    os.path.join(folder, "index.html"), "w", encoding="utf-8"
                ) as file:
                    file.write(content)

                await download_resources(
                    BeautifulSoup(content, "html.parser"), url, folder, session, debug
                )
    except Exception as e:
        logger.error(f"Error downloading page {url}: {e}")
        if debug:
            from traceback import format_exc

            logger.error(format_exc())
        return

    logger.info(f"Page {url} downloaded successfully.")


async def download_resources(soup, base_url, folder, session, debug):
    tasks = [
        save_resource(urljoin(base_url, resource.get(attr)), folder, session, debug)
        for tag, attr in {"img": "src", "link": "href", "script": "src"}.items()
        for resource in soup.find_all(tag)
        if resource.get(attr)
    ]
    debug and logger.debug(f"Downloading {len(tasks)} resources")
    await asyncio.gather(*tasks)


async def save_resource(url, folder, session, debug):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                resource_path = await create_directory_for_resource(url, folder)
                with open(resource_path, "wb") as file:
                    file.write(await response.read())
                debug and logger.debug(f"Resource {url} saved to {resource_path}")
    except Exception as e:
        logger.error(f"Error downloading resource {url}: {e}")