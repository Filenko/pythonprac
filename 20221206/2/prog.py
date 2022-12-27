import sys
import asyncio
from copy import copy

tasks = []

async def merge(a, b, start, mid, finish, event_in1, event_in2, event_out):
    await event_in1.wait()
    await event_in2.wait()

    cnt, i, j = start, start, mid
    a = a.copy()

    while i < mid and j < finish:
        if a[i] < a[j]:
            b[cnt] = a[i]
            i += 1
            cnt += 1
        else:
            b[cnt] = a[j]
            j += 1
            cnt += 1

    while i < mid:
        b[cnt] = a[i]
        cnt += 1
        i += 1

    while j < finish:
        b[cnt] = a[j]
        cnt += 1
        j += 1

    event_out.set()


async def mtasks(A):
    res = copy(A)

    def task_(l, r, event):
        if r - l < 2:
            event.set()
            return
        event_in1 = asyncio.Event()
        event_in2 = asyncio.Event()
        task = asyncio.create_task(merge(res, res, l, (r + l) // 2, r, event_in1, event_in2, event))
        tasks.insert(0, task)
        task_(l, (l + r) // 2, event_in1)
        task_((l + r) // 2, r, event_in2)
        return tasks

    return task_(0, len(res), asyncio.Event()), res


exec(sys.stdin.read())
