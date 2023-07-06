import asyncio
import requests
import http3


def cat_request_sync():
    url = "https://api.thecatapi.com/v1/images/search?limit=10"
    jsons = requests.get(url).json()
    for d in jsons:
        url = d.get('url')
        name = d.get('id')
        with open(f"./cats/{name}.jpg", "wb") as f:
            f.write(requests.get(url).content)


async def cat_request_async(n):
    url = "https://api.thedogapi.com/v1/images/search"
    async with http3.AsyncClient() as client:
        print(f"Requesting the dog batch number {n}")
        r = await client.get(url)
        jsons = r.json()
        for i, dictionary in enumerate(jsons):
            url = dictionary.get('url')
            name = dictionary.get('id')
            extension = url.split(".")[-1]
            with open(f"./dogs/{name}.{extension}", "wb") as f:
                print(f"Requesting the image {n}-{i}")
                c = await client.get(url)
                f.write(c.content)
        print(f"The dog batch number {n} is ready")


async def main():
    routines = [cat_request_async(i) for i in range(0, 1)]
    await asyncio.gather(*routines)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
