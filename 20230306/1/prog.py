import cowsay
from io import StringIO
import shlex
import cmd

pos = 0, 0
field = [[None for i in range(10)] for j in range(10)]
weapons = {"sword": 10, "spear": 15, "axe": 20}


jgsbat = cowsay.read_dot_cow(StringIO(r"""
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


def move(direction):
    global pos
    move_direction = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
    x = pos[0] + move_direction[direction][0]
    x += 10 if x < 0 else 0 + -10 if x > 9 else 0
    y = pos[1] + move_direction[direction][1]
    y += 10 if y < 0 else 0 + -10 if y > 9 else 0
    pos = x, y
    print(f"Moved to {pos}")


def addmon(x, y, name, hello, hp):
    if name not in cowsay.list_cows():
        print("Cannot add unknown monster")
        return
    global field
    wasMonsterHere = field[x][y]
    field[x][y] = {"greeting": hello, "name": name, "hp": hp}
    print(f"Added monster {name} to {x}, {y} saying {hello}")
    if wasMonsterHere:
        print("Replaced the old monster")


def encounter():
    global field, pos
    if field[pos[0]][pos[1]]:
        print(cowsay.cowsay(field[pos[0]][pos[1]]["greeting"], cow=field[pos[0]][pos[1]]["name"]))


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


def attack(weapon):
    global field, pos
    curPosField = field[pos[0]][pos[1]]
    if curPosField is None:
        print("No monster here")
        return

    damage = weapons[weapon]
    field[pos[0]][pos[1]]["hp"] -= damage
    realDamage = damage if field[pos[0]][pos[1]]["hp"] >= 0 else damage - abs(field[pos[0]][pos[1]]["hp"])

    print(f'Attacked {field[pos[0]][pos[1]]["name"]}, damage {realDamage} hp')
    if field[pos[0]][pos[1]]["hp"] <= 0:
        print(f'{field[pos[0]][pos[1]]["name"]} died')
        field[pos[0]][pos[1]] = None
    else:
        print(f'{field[pos[0]][pos[1]]["name"]} now has {field[pos[0]][pos[1]]["hp"]}')


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

        args = shlex.split(args)
        weapon = "sword"
        if args and args[0] == "with":
            if args[1] in weapons:
                weapon = args[1]
            else:
                print("Unknown weapon")
                return

        attack(weapon)

    def complete_attack(self, text, line, begidx, endidx):

        if (not text and len(shlex.split(line)) == 1) or (text and len(shlex.split(line)) == 2):
            return ["with"]
        elif (not text and len(shlex.split(line)) == 2) or (text and len(shlex.split(line)) == 3):
            return [w for w in weapons if w.startswith(text)]





MUD().cmdloop()

