import html

import aiofiles as aiofiles
import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://historyofenglishpodcast.com/episodes/"
        print(f"Getting the front page")
        async with session.get(url) as r:
            txt = await r.text()
        soup = BeautifulSoup(txt, features="html.parser")
        soup = soup.find("div", {"class": "entry-content"})
        hrefs = []
        for a in soup.findAll("a"):
            hrefs.append(a.get("href"))
        tasks = []
        for href in hrefs:
            tasks.append(download_episode(session, href))
        await asyncio.gather(*tasks)


async def download_episode(session, href):
    print(f"Getting the page: {href}")
    async with session.get(href) as r:
        txt = await r.text()
    soup = BeautifulSoup(txt, features="html.parser")
    try:
        h1 = soup.find("h1", {"class": "entry-title"})
        name = h1.text.replace(":", "-").replace("?", "(que)")
        a = soup.find("a", {"title": "Download"})
    except AttributeError as e:
        print(href)
        raise e
    href = a.get("href")
    print(f"Downloading {name}.mp3")
    async with session.get(href) as r:
        contents = await r.content.read()
        async with aiofiles.open(f"./podcast/{name}.mp3", "wb") as f:
            await f.write(contents)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
