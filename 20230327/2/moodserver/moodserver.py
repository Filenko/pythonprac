"""Mood server."""

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
positions = {}
monsters = []
weapons = {"sword": 10, "spear": 15, "axe": 20}
userMonsters = {"jgsbat": jgsbat}


# monsters = [{pos: (0,0), hp: int, hello: string}]

def checkMonsters(pos):
    global monsters
    for monster in enumerate(monsters):
        if monster[1]["pos"] == pos:
            return monster[0]
    return -1
def move(xDir, yDir, pos):
    """Move to right by xDir and to left by yDir."""
    x = pos[0] + xDir
    x += 10 if x < 0 else 0 + -10 if x > 9 else 0
    y = pos[1] + yDir
    y += 10 if y < 0 else 0 + -10 if y > 9 else 0
    pos = (x, y)
    return [f"Moved to {pos}", pos]



def addmon(x, y, name, hello, hp):
    """Add monster with name, hp and message."""
    response = []
    sendAll = True
    if name not in cowsay.list_cows() and name not in userMonsters:
        response.append("Cannot add unknown monster")
        sendAll = False

    global monsters
    monsterHere = checkMonsters((x,y))

    if monsterHere != -1:
        monsters[monsterHere] = {"greeting": hello, "name": name, "hp": hp, "pos": (x,y)}
    else:
        monsters.append({"pos":(x,y),"greeting": hello, "name": name, "hp": hp})

    response.append(f"Added monster {name} to {x}, {y} saying {hello}")
    if monsterHere != -1:
        response.append("Replaced the old monster")
        sendAll = False

    return response, sendAll


def encounter(pos):
    """Check if here is monster and return its message."""
    global monsters

    if (monsterId := checkMonsters(pos)) != -1:
        hello = monsters[monsterId]["greeting"]
        name = monsters[monsterId]["name"]
        if name in cowsay.list_cows():
            return cowsay.cowsay(hello, cow=name)
        if name in cowsay.list_cows():
            return cowsay.cowsay(hello, cowfile=userMonsters[name])
    else:
        print(f"NO MONSTER AT {pos}")
    return None


def attack(name, weapon, pos):
    """Attack monster with different weapons (damage)."""
    global monsters
    monsterHere = checkMonsters(pos)
    response = []
    sendAll = True
    if (monsterHere == -1) or (monsters[monsterHere]["name"] != name):
        response.append(f'No {name} here')
        sendAll = False
        return response, sendAll

    damage = weapons[weapon]
    monsters[monsterHere]["hp"] -= damage
    realDamage = damage if monsters[monsterHere]["hp"] >= 0 else damage - abs(monsters[monsterHere]["hp"])

    response.append(f'Attacked {monsters[monsterHere]["name"]}, damage {realDamage} hp')
    if monsters[monsterHere]["hp"] <= 0:
        response.append(f'{monsters[monsterHere]["name"]} died')
        monsters.pop(monsterHere)
    else:
        response.append(f'{monsters[monsterHere]["name"]} now has {monsters[monsterHere]["hp"]}')

    return response, sendAll


async def sendMessage(msg, me=None):
    """Send message to all clients or to single one."""
    if not me:
        for client in clients:
            await clients[client].put(msg)
    else:
        await clients[me].put(msg)


async def MUDhandler(reader, writer):
    """Start the game and provide all logic."""
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
                            positions[me] = (0,0)
                            await sendMessage(f"{nickname} join to MUD")
                    case ["move", x, y]:
                        req, newPos = move(int(x), int(y), positions[me])
                        req = [req]
                        positions[me] = newPos
                        print(f"{nicknames[me]} NEWPOS", newPos)
                        if e := encounter(newPos):
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
                        req, sendAll = attack(name, weapon, positions[me])
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
    """Start server with main function."""
    server = await asyncio.start_server(MUDhandler, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
