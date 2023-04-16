import asyncio
import cowsay
import io

jgsbat = cowsay.read_dot_cow(io.StringIO(r"""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\\\'--'//__
         (((""`  `"")))
EOC
"""))

clients = {}
nicknames = {}
pos = 0, 0
field = [[None for i in range(10)] for j in range(10)]
weapons = {"sword": 10, "spear": 15, "axe": 20}
userMonsters = {"jgsbat": jgsbat}


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
    sendAll = True
    if name not in cowsay.list_cows() and name not in userMonsters:
        response.append("Cannot add unknown monster")
        sendAll = False

    global field
    wasMonsterHere = field[x][y]
    field[x][y] = {"greeting": hello, "name": name, "hp": hp}
    response.append(f"Added monster {name} to {x}, {y} saying {hello}")
    if wasMonsterHere:
        response.append("Replaced the old monster")
        sendAll = False

    return response, sendAll


def encounter():
    global field, pos
    response = []
    if field[pos[0]][pos[1]]:
        hello = field[pos[0]][pos[1]]["greeting"]
        name = cow = field[pos[0]][pos[1]]["name"]
        if name in cowsay.list_cows():
            return cowsay.cowsay(hello,cow=name)
        if name in cowsay.list_cows():
            return cowsay.cowsay(hello,cowfile=userMonsters[name])
    return None


def attack(name, weapon):
    global field, pos
    curPosField = field[pos[0]][pos[1]]
    response = []
    sendAll = True
    if curPosField is None or curPosField["name"] != name:
        response.append(f'No {name} here')
        sendAll = False
        return response, sendAll

    damage = weapons[weapon]
    field[pos[0]][pos[1]]["hp"] -= damage
    realDamage = damage if field[pos[0]][pos[1]]["hp"] >= 0 else damage - abs(field[pos[0]][pos[1]]["hp"])

    response.append(f'Attacked {field[pos[0]][pos[1]]["name"]}, damage {realDamage} hp')
    if field[pos[0]][pos[1]]["hp"] <= 0:
        response.append(f'{field[pos[0]][pos[1]]["name"]} died')
        field[pos[0]][pos[1]] = None
    else:
        response.append(f'{field[pos[0]][pos[1]]["name"]} now has {field[pos[0]][pos[1]]["hp"]}')

    return response, sendAll


async def sendMessage(msg, me=None):
    if not me:
        for client in clients:
            await clients[client].put(msg)
    else:
        await clients[me].put(msg)


async def MUDhandler(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                print(q.result().decode().split())
                match q.result().decode().split():
                    case ["login", nickname]:
                        if nickname in nicknames.values():
                            await sendMessage("This nickname is already taken!", me)
                        else:
                            nicknames[me] = nickname
                            await sendMessage(f"{nickname} join to MUD")
                    case ["move", x, y]:
                        req = move(int(x), int(y))
                        if e := encounter():
                            req.append(e)
                        print(req, x, y)
                        await sendMessage("\n".join(req), me)
                    case ["addmon", x, y, name, hp, *hello]:
                        hello = " ".join(hello)
                        req, sendAll = addmon(int(x), int(y), name, hello, int(hp))
                        if sendAll:
                            await sendMessage("\n".join(req))
                        else:
                            await sendMessage("\n".join(req), me)

                    case ["attack", name, weapon]:
                        req, sendAll = attack(name, weapon)
                        if sendAll:
                            await sendMessage("\n".join(req))
                        else:
                            await sendMessage("\n".join(req), me)

                    case ["sayall", *msg]:
                        msg = " ".join(msg)
                        await sendMessage(f"\n{nicknames[me]}:{msg}")

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(MUDhandler, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
