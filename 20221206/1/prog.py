import asyncio

end = asyncio.Event()


async def writer(q, d):
    i = 0
    while True:
        await asyncio.sleep(d)
        await q.put(f"{i}_{d}")
        if end.is_set():
            break
        i += 1


async def stacker(q, s):
    while True:
        el = await q.get()
        await s.put(el)
        if end.is_set():
            break


async def reader(s, n, d):
    for i in range(n):
        await asyncio.sleep(d)
        el = await s.get()
        print(el)
    end.set()


async def main():
    d1, d2, d3, n = eval(input())
    q, s = asyncio.Queue(), asyncio.LifoQueue()
    await asyncio.gather(
        writer(q, d1),
        writer(q, d2),
        stacker(q, s),
        reader(s, n, d3)
    )


asyncio.run(main())
