# ✨WebCopy

**WebCopy** is a Python project that allows you to download the contents of any website, including HTML, images, CSS, and other assets

## Features
- Asynchronous downloading of website content
- Saves all assets (HTML, CSS, images, etc.) in the appropriate folder structure
- Folder named after the website's domain (e.g., `example.com`)
- Easy to use: just enter the URL of the website

## Installation
To get started with WebCopy, you'll need to install the required dependencies. You can do this by running the following command:

```bash
pip install -r requirements.txt
```

## Usage
After installing the necessary libraries, you can run the script and input any website URL to copy its contents.

```bash
python webcopy.py
```
The script will prompt you to enter the URL of the website you want to copy. The content will be saved in a folder named after the domain of the website.

## Example
```bash
Enter the URL of the website: https://example.com
```
This will create a folder named example.com in your current directory, containing the website's HTML and assets in their respective subfolders.

## Requirements
- Python 3.7+
- aiohttp
- beautifulsoup4