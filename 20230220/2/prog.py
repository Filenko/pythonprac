import cowsay

pos = 0, 0
field = [[None for i in range(10)] for j in range(10)]


def move(direction):
    global pos
    move_direction = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
    x = pos[0] + move_direction[direction][0]
    x += 10 if x < 0 else 0 + -10 if x > 9 else 0
    y = pos[1] + move_direction[direction][1]
    y += 10 if y < 0 else 0 + -10 if y > 9 else 0
    pos = x, y
    print(f"Moved to {pos}")


def addmon(x, y, name, hello):
    if name not in cowsay.list_cows():
        print("Cannot add unknown monster")
    global field
    wasMonsterHere = field[x][y]
    field[x][y] = hello, name
    print(f"Added monster {name} to {x}, {y} saying {hello}")
    if wasMonsterHere:
        print("Replaced the old monster")


def encounter():
    global field, pos
    if field[pos[0]][pos[1]]:
        print(cowsay.cowsay(field[pos[0]][pos[1]][0], cow=field[pos[0]][pos[1]][1]))


while s := input():
    match s.split():
        case ["up" | "down" | "left" | "right"]:
            move(s.split()[0])
            encounter()
        case ["addmon", name, x, y, hello]:
            if not str.isdigit(x) or not str.isdigit(y):
                print("Invalid arguments!")
            else:
                addmon(int(x), int(y), hello)
        case _:
            print("Invalid arguments!")
