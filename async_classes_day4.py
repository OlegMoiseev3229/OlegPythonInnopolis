import asyncio
import random as rnd

class Countdown:
    def __init__(self, a, b, name):
        self.a = a
        self.b = b
        self.name = name

    def _ready(self):
        print(f"{self.name}: Done")

    async def start(self):
        self._ready()


class SteadyCountdown(Countdown):
    def __init__(self, a, b, name):
        super(SteadyCountdown, self).__init__(a, b, name)

    async def start(self):
        for i in range(max(self.a, self.b), min(self.a, self.b), -1):
            print(f"{self.name}: {i}")
            await asyncio.sleep(1)
        await super().start()


class CrazyCountdown(Countdown):
    def __init__(self, a, b, name, range_of_times=(0.2, 3)):
        self.range_of_times = range_of_times
        super().__init__(a, b, name)

    async def start(self):
        for i in range(max(self.a, self.b), min(self.a, self.b), -1):
            print(f"{self.name}: {i}")
            min_t = self.range_of_times[0]
            max_t = self.range_of_times[1]
            await asyncio.sleep(rnd.random()*(max_t - min_t) + min_t)
        await super().start()


class KamikazeCountdown(SteadyCountdown):
    def _ready(self):
        raise ValueError('BOOM!')


async def main():
    await KamikazeCountdown(10, 0, "Kamikaze").start()


if __name__ == '__main__':
    asyncio.run(main())