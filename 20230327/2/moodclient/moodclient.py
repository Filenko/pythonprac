"""Mood client."""

import socket
import sys
import threading
import cmd
import shlex
import cowsay

recieving = True
weapons = {"sword": 10, "spear": 15, "axe": 20}
userMonsters = {"jgsbat"}


def parse_addmon_arguments(args):
    """Parse arguments of addmon function."""
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


def request(req):
    """Make request to server."""
    global socketCow
    socketCow.send(f"{req}\n".encode())


def recieve(prompt="> "):
    """Revieve data from server."""
    global recieving
    global socketCow
    while recieving:
        msg = socketCow.recv(1024).decode()
        print(f"{msg.strip()}\n{prompt}", end="", flush=True)


class MUD(cmd.Cmd):
    """Main class for game."""

    intro = "<<< Welcome to Python-MUD 0.1 >>>"
    prompt = "> "

    def do_up(self, args):
        """Move 1 up."""
        request("move 0 -1")

    def do_down(self, args):
        """Move 1 down."""
        request("move 0 1")

    def do_left(self, args):
        """Move 1 left."""
        request("move -1 0")

    def do_right(self, args):
        """Move 1 right."""
        request("move 1 0")

    def do_addmon(self, args):
        """Add monster."""
        if len(args) < 3:
            print("Invalid arguments!")
            return
        name, *args = shlex.split(args)
        if args := parse_addmon_arguments(args):
            x, y, hello, hp = args
            request(f"addmon {x} {y} {name} {hp} {hello}")

    def do_attack(self, args):
        """Attack monster."""
        if len(args) < 2:
            print("Specify monster name")
            return
        name, *args = shlex.split(args)
        weapon = "sword"
        if args and args[0] == "with":
            if args[1] in weapons:
                weapon = args[1]
            else:
                print("Unknown weapon")
                return

        request(f"attack {name} {weapon}")

    def do_sayall(self, args):
        """Say something to all users."""
        if len(args) < 1:
            print("Specify text to say to all")
            return
        msg = args[0:]
        request(f"sayall {msg}")

    def do_exit(self, args):
        """Exit."""
        global recieving
        request("exit")
        recieving = False
        global reciever

        return True

    def complete_attack(self, text, line, begidx, endidx):
        """Tab-completion for attack command."""
        if (not text and len(shlex.split(line)) == 1) or (text and len(shlex.split(line)) == 2):
            return [name for name in (cowsay.list_cows() + list(userMonsters.keys())) if name.startswith(text)]
        elif (not text and len(shlex.split(line)) == 2) or (text and len(shlex.split(line)) == 3):
            return ["with"]
        elif (not text and len(shlex.split(line)) == 3) or (text and len(shlex.split(line)) == 4):
            return [w for w in weapons if w.startswith(text)]


def main():
    """Сonnect to server, register and start cmd."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketCow:
        socketCow.connect(("localhost", 1337))
        if nickname := sys.argv[1]:
            request(f"login {nickname}")
            ans = socketCow.recv(1024).decode()
            if ans.strip() != "This nickname is already taken!":
                cmdline = MUD()
                reciever = threading.Thread(target=recieve)
                reciever.start()
                cmdline.cmdloop()
            else:
                print("This nickname is already taken!")
        else:
            print("Enter a nickname to join MUD")
