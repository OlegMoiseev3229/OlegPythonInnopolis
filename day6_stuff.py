import socketio
import asyncio


async def main():
    sio = socketio.AsyncClient()
    await sio.connect("https://online-go.com/")
    sid = sio.sid
    print(sid)

    @sio.on('*')
    async def catch_all(event, data):
        print(f"{event=}, {data=}")


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
