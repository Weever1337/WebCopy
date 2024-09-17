import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


async def create_directory_for_resource(resource_url, folder):
    parsed_url = urlparse(resource_url)
    resource_path = parsed_url.path.lstrip("/")
    resource_folder = os.path.join(folder, os.path.dirname(resource_path))

    if not os.path.exists(resource_folder):
        os.makedirs(resource_folder)

    return os.path.join(resource_folder, os.path.basename(resource_path))


async def download_page(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Error fetching {url}")
                return

            page_name = os.path.join(folder, "index.html")
            content = await response.text()
            with open(page_name, "w", encoding="utf-8") as file:
                file.write(content)

            soup = BeautifulSoup(content, "html.parser")
            await download_resources(soup, url, folder, session)

    print(f"Page {url} downloaded successfully.")


async def download_resources(soup, base_url, folder, session):
    tasks = []
    tags = {"img": "src", "link": "href", "script": "src"}

    for tag, attr in tags.items():
        for resource in soup.find_all(tag):
            resource_url = resource.get(attr)
            if resource_url:
                full_url = urljoin(base_url, resource_url)
                tasks.append(save_resource(full_url, folder, session))

    await asyncio.gather(*tasks)


async def save_resource(url, folder, session):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                resource_path = await create_directory_for_resource(url, folder)
                content = await response.read()
                with open(resource_path, "wb") as file:
                    file.write(content)
                print(f"Resource {url} saved to {resource_path}.")
    except Exception as e:
        print(f"Error downloading resource {url}: {e}")


if __name__ == "__main__":
    url = input("Enter the URL of the website: ")
    parsed_url = urlparse(url)
    folder_name = parsed_url.netloc

    asyncio.run(download_page(url, folder_name))
