"""Mood server."""

import asyncio
import cowsay
import io
import random

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
    """
    Check if a monster is present at the given position.

    Args:
        pos (tuple): A tuple representing the position to check.

    Returns:
        int: The index of the monster if present, -1 otherwise.
    """
    global monsters
    for monster in enumerate(monsters):
        if monster[1]["pos"] == pos:
            return monster[0]
    return -1


def move(xDir, yDir, pos):
    """
    Move to a new position based on the given directions.

    Args:
        xDir (int): The direction to move in the x-axis.
        yDir (int): The direction to move in the y-axis.
        pos (tuple): The current position.

    Returns:
        list: A list containing a message about the move and the new position.
    """
    x = pos[0] + xDir
    x += 10 if x < 0 else 0 + -10 if x > 9 else 0
    y = pos[1] + yDir
    y += 10 if y < 0 else 0 + -10 if y > 9 else 0
    pos = (x, y)
    return [f"Moved to {pos}", pos]


def addmon(x, y, name, hello, hp):
    """
    Add a monster with a given name, greeting message, and health points at a specific position.

    Args:
        x (int): The x-coordinate of the position.
        y (int): The y-coordinate of the position.
        name (str): The name of the monster.
        hello (str): The greeting message of the monster.
        hp (int): The health points of the monster.

    Returns:
        tuple: A tuple containing a list of response messages and a boolean indicating whether to send to all clients.
    """
    response = []
    sendAll = True
    if name not in cowsay.list_cows() and name not in userMonsters:
        response.append("Cannot add unknown monster")
        sendAll = False

    global monsters
    monsterHere = checkMonsters((x, y))

    if monsterHere != -1:
        monsters[monsterHere] = {"greeting": hello, "name": name, "hp": hp, "pos": (x, y)}
    else:
        monsters.append({"pos": (x, y), "greeting": hello, "name": name, "hp": hp})

    response.append(f"Added monster {name} to {x}, {y} saying {hello}")
    if monsterHere != -1:
        response.append("Replaced the old monster")
        sendAll = False

    return response, sendAll


def encounter(pos):
    """
    Check if a monster is present at the given position and return its greeting message.

    Args:
        pos (tuple): The position to check.

    Returns:
        str: The greeting message of the monster if present, None otherwise.
    """
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
    """
    Attack a monster with a specific weapon at a given position.

    Args:
        name (str): The name of the monster.
        weapon (str): The weapon to use for the attack.
        pos (tuple): The position of the attack.

    Returns:
        tuple: A tuple containing a list of response messages and a boolean indicating whether to send to all clients.
    """
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
    """
    Send a message to all clients or to a single client.

    Args:
        msg (str): The message to send.
        me (str): The identifier of the client to send the message to. If None, the message is sent to all clients.

    Returns:
        None
    """
    if not me:
        for client in clients:
            await clients[client].put(msg)
    else:
        await clients[me].put(msg)


async def moveMonster():
    """
    Move a random monster in a random direction and encounter players.

    This function runs indefinitely, moving a random monster every 30 seconds.

    Returns:
        None
    """
    global clients, positions, monsters
    dirs = {
        (1, 0): "right",
        (0, 1): "down",
        (-1, 0): "left",
        (0, -1): "up"
    }
    while True:
        await asyncio.sleep(30)
        if len(monsters) == 0:
            continue

        success = False
        while not success:
            monster = random.randint(0, len(monsters) - 1)
            monsterPos = monsters[monster]["pos"]
            direction = random.choice(list(dirs.keys()))
            directionName = dirs[direction]
            newMonsterPos = move(direction[0], direction[1], monsterPos)[1]
            if checkMonsters(newMonsterPos) == -1:
                monsters[monster]["pos"] = newMonsterPos
                success = True

        for client in clients:
            msg = [f'{monsters[monster]["name"]} moved one cell {directionName}']
            if enc := encounter(positions[client]):
                msg.append(enc)
            await clients[client].put("\n".join(msg))


async def MUDhandler(reader, writer):
    """
    Handle a client connection for the MUD game.

    This function reads commands from the client, processes them, and sends responses back to the client.

    Args:
        reader (StreamReader): The stream reader object for reading data from the client.
        writer (StreamWriter): The stream writer object for sending data to the client.

    Returns:
        None
    """
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
                            positions[me] = (0, 0)
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
    """
    Start the server and the MUD game.

    This function starts the server, waits for client connections, and starts the game logic.

    Returns:
        None
    """
    server = await asyncio.start_server(MUDhandler, '0.0.0.0', 1337)
    async with server:
        await asyncio.gather(server.serve_forever(), moveMonster())
