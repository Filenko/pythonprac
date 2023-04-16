import asyncio
import socket
import shlex
import cmd

import cowsay

weapons = {"sword": 10, "spear": 15, "axe": 20}
userMonsters = {"jgsbat"}
def parse_addmon_arguments(args):
    if len(args) != 7:
        print("Invalid arguments!")
        return None

    requiredArguments = ["hello", "hp", "coords"]
    argumentsExist = [x in args for x in requiredArguments]
    if not all(argumentsExist):
        print("Invalid arguments!")
        return None
    x, y = args[args.index("coords") + 1], args[args.index("coords") + 2]
    hp = args[args.index("hp") + 1]
    hello = args[args.index("hello") + 1]

    return int(x), int(y), hello, int(hp)

def request(s):
    global socketCow
    socketCow.send(f"{s}\n".encode())
    ans = socketCow.recv(1024).decode().strip()
    for l in ans.split("\n"):
        if l.startswith("SAY"):
            l = l.split()
            say = l[0]
            name = l[1]
            msg = " ".join(l[2:])
            if name in cowsay.list_cows():
                print(cowsay.cowsay(msg, cow=name))
            elif name in userMonsters:
                print(cowsay.cowsay(msg, cowfile=userMonsters[name]))
        else:
            print(l)

class MUD(cmd.Cmd):
    intro = "<<< Welcome to Python-MUD 0.1 >>>"
    prompt = "> "

    def do_up(self, args):
        request("move 0 -1")


    def do_down(self, args):
        request("move 0 1")

    def do_left(self, args):
        request("move -1 0")

    def do_right(self, args):
        request("move 1 0")

    def do_addmon(self, args):
        if len(args) < 3:
            print("Invalid arguments!")
            return
        name, *args = shlex.split(args)
        if args := parse_addmon_arguments(args):
            x, y, hello, hp = args
            request(f"addmon {x} {y} {name} {hp} {hello}")

    def do_attack(self, args):
        name, *args = shlex.split(args)
        weapon = "sword"
        if args and args[0] == "with":
            if args[1] in weapons:
                weapon = args[1]
            else:
                print("Unknown weapon")
                return

        request(f"attack {name} {weapon}")

    def complete_attack(self, text, line, begidx, endidx):

        if (not text and len(shlex.split(line)) == 1) or (text and len(shlex.split(line)) == 2):
            return [name for name in (cowsay.list_cows() + list(userMonsters.keys())) if name.startswith(text)]
        elif (not text and len(shlex.split(line)) == 2) or (text and len(shlex.split(line)) == 3):
            return ["with"]
        elif (not text and len(shlex.split(line)) == 3) or (text and len(shlex.split(line)) == 4):
            return [w for w in weapons if w.startswith(text)]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketCow:
    socketCow.connect(("0.0.0.0", 1234))
    MUD().cmdloop()



