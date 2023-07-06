import asyncio
import io

import aiohttp
import tkinter as tk
from PIL import Image, ImageTk
import os

pointer = 0


class AnimalAPIRequester:
    def __init__(self, api):
        self.api = api
        if self.api == "cat":
            self.url = "https://api.thecatapi.com/v1/images/search?limit={}"
        elif self.api == "dog":
            self.url = "https://api.thedogapi.com/v1/images/search?limit={}"
        else:
            raise ValueError("API must be either 'cat' or 'dog'")

    async def get(self, limit):
        if limit > 10:
            raise ValueError("Limit should be <= 10")
        elif limit < 1:
            raise ValueError("Limit should be >= 1")
        url = self.url.format(limit)
        async with aiohttp.client.ClientSession() as session:
            async with session.get(url) as response:
                jsons = await response.json()
                images = []
                for i, j in enumerate(jsons):
                    url = j.get('url')
                    name = j.get('id')
                    print(f"Getting {name}")
                    async with session.get(url) as c:
                        contents = await c.content.read()
                        im = Image.open(io.BytesIO(contents))
                        images.append(im)
        return images

    async def get_and_save(self, limit=1, folder=None, names=None):
        if folder is None:
            folder = self.api + "s"
        if names is None:
            names = [self.api+str(i)+".png" for i in range(0, limit)]
        if len(names) < limit:
            names = [n for n in names].extend([self.api + str(i)+".png" for i in range(len(names), limit)])
        for i, n in enumerate(names):
            if len(n.split(".")) == 1:
                names[i] = n + ".png"
        images = await self.get(limit)
        for i, im in enumerate(images):
            try:
                print(f"Saving {os.path.join(folder, names[i])}")
                im.save(os.path.join(folder, names[i]))
            except IndexError:
                break


async def request_cat(n):
    url = "https://api.thecatapi.com/v1/images/search?limit=10"
    print(f"Requesting the cat batch number {n}")
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            jsons = await response.json()
            for i, j in enumerate(jsons):
                url = j.get('url')
                name = j.get('id')
                extension = url.split(".")[-1]
                with open(f"./cats/{name}.{extension}", "wb") as f:
                    print(f"Requesting the image {n}-{i}: {name}")
                    async with session.get(url) as c:
                        contents = c.content
                        f.write(await contents.read())
        print(f"The cat batch number {n} is ready")


async def main():
    dog_getter = AnimalAPIRequester('dog')
    await asyncio.gather(*[dog_getter.get_and_save(5, "dogs2", [f"Red-headed_{i}", f"Rex_{i}", f"King_{i}",
                                                                f"Kynning_{i}", f"Caesar_{i}"])
                           for i in range(10)])


def display_cats():
    global pointer
    root = tk.Tk()
    image_view = tk.Label(root, width=600, height=600)
    images = []
    pointer = 0
    for path in os.scandir("./cats"):
        name = path.name
        extension = name.split(".")[-1]
        im = Image.open(os.path.join(path))
        wanted_size = 600
        scale = min(wanted_size / im.size[0], wanted_size / im.size[1])
        im = im.resize((int(im.size[0] * scale), int(im.size[1] * scale)))
        images.append(ImageTk.PhotoImage(im))

    def set_image(im):
        image_view.config(image=im)

    def go_left():
        global pointer
        pointer -= 1
        pointer %= len(images)
        set_image(images[pointer])

    def go_right():
        global pointer
        pointer += 1
        pointer %= len(images)
        set_image(images[pointer])

    button_right = tk.Button(root, text=">>>", command=go_right)
    button_left = tk.Button(root, text="<<<", command=go_left)
    set_image(images[0])
    image_view.grid(row=0, columnspan=2)
    button_left.grid(row=1, column=0)
    button_right.grid(row=1, column=1)
    root.mainloop()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #asyncio.run(main())
    display_cats()

