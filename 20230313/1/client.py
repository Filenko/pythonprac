import asyncio
import socket

pos = 0, 0
field = [[None for i in range(10)] for j in range(10)]
weapons = {"sword": 10, "spear": 15, "axe": 20}
userMonsters = {"jgsbat"}
class MUD(cmd.Cmd):
    intro = "<<< Welcome to Python-MUD 0.1 >>>"
    prompt = "> "

    def do_up(self, args):
        move("up")
        encounter()

    def do_down(self, args):
        move("down")
        encounter()

    def do_left(self, args):
        move("left")
        encounter()

    def do_right(self, args):
        move("right")
        encounter()

    def do_addmon(self, args):
        if len(args) < 3:
            print("Invalid arguments!")
            return

        name, *args = shlex.split(args)
        if args := parse_addmon_arguments(args):
            x, y, hello, hp = args
            addmon(x, y, name, hello, hp)

    def do_attack(self, args):

        name, *args = shlex.split(args)
        weapon = "sword"
        if args and args[0] == "with":
            if args[1] in weapons:
                weapon = args[1]
            else:
                print("Unknown weapon")
                return
        attack(name, weapon)

    def complete_attack(self, text, line, begidx, endidx):

        if (not text and len(shlex.split(line)) == 1) or (text and len(shlex.split(line)) == 2):
            return [name for name in (cowsay.list_cows() + list(userMonsters.keys())) if name.startswith(text)]
        elif (not text and len(shlex.split(line)) == 2) or (text and len(shlex.split(line)) == 3):
            return ["with"]
        elif (not text and len(shlex.split(line)) == 3) or (text and len(shlex.split(line)) == 4):
            return [w for w in weapons if w.startswith(text)]


MUD().cmdloop()
