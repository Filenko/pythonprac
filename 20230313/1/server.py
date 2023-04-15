import asyncio
import pickle

import cowsay
import shlex

pos = 0, 0
field = [[None for i in range(10)] for j in range(10)]
weapons = {"sword": 10, "spear": 15, "axe": 20}
userMonsters = {"jgsbat"}


def move(xDir, yDir):
    global pos
    x = pos[0] + xDir
    x += 10 if x < 0 else 0 + -10 if x > 9 else 0
    y = pos[1] + yDir
    y += 10 if y < 0 else 0 + -10 if y > 9 else 0
    pos = x, y
    return [f"Moved to {pos}"]


def addmon(x, y, name, hello, hp):
    response = []
    if name not in cowsay.list_cows() and name not in userMonsters:
        response.append("Cannot add unknown monster")
        return
    global field
    wasMonsterHere = field[x][y]
    field[x][y] = {"greeting": hello, "name": name, "hp": hp}
    response.append(f"Added monster {name} to {x}, {y} saying {hello}")
    if wasMonsterHere:
        response.append("Replaced the old monster")
    return response


def encounter():
    global field, pos
    response = []
    if field[pos[0]][pos[1]]:
        hello = field[pos[0]][pos[1]]["greeting"]
        name = cow = field[pos[0]][pos[1]]["name"]
        return f"SAY {name} {hello}"
    return None


def attack(name, weapon):
    global field, pos
    curPosField = field[pos[0]][pos[1]]
    response = []
    if curPosField is None or curPosField["name"] != name:
        response.append(f'No {name} here')
        return

    damage = weapons[weapon]
    field[pos[0]][pos[1]]["hp"] -= damage
    realDamage = damage if field[pos[0]][pos[1]]["hp"] >= 0 else damage - abs(field[pos[0]][pos[1]]["hp"])

    response.append(f'Attacked {field[pos[0]][pos[1]]["name"]}, damage {realDamage} hp')
    if field[pos[0]][pos[1]]["hp"] <= 0:
        response.append(f'{field[pos[0]][pos[1]]["name"]} died')
        field[pos[0]][pos[1]] = None
    else:
        response.append(f'{field[pos[0]][pos[1]]["name"]} now has {field[pos[0]][pos[1]]["hp"]}')
    return response


async def serv(reader, writer):
    host, _ = writer.get_extra_info('peername')
    print(host, _)
    while not reader.at_eof():
        request = await reader.readline()
        request = request.strip().decode()
        print(shlex.split(request))
        match shlex.split(request):
            case ["move", x, y]:
                req = move(int(x), int(y))
                if e := encounter():
                    req.append(e)
                print(req)
            case ["addmon", x, y, name, hp, *hello]:
                hello = " ".join(hello)
                req = addmon(int(x), int(y), name, hello, int(hp))
                print("REASFA", req)
            case ["attack", name, weapon]:
                req = attack(name, weapon)
                print(req)
        req = "\n".join(req)
        writer.write(req.encode())

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(serv, '0.0.0.0', 1234)
    async with server:
        await server.serve_forever()


asyncio.run(main())
