class Undead(Exception):
    pass


class Skeleton(Undead):
    pass


class Zombie(Undead):
    pass


class Ghoul(Undead):
    pass


def necro(a):
    if a % 3 == 0:
        raise Skeleton
    if a % 3 == 1:
        raise Zombie
    if a % 3 == 2:
        raise Ghoul


x, y = eval(input())

for i in range(x, y):
    try:
        necro(i)
    except Skeleton:
        print("Skeleton")
    except Zombie:
        print("Zombie")
    except Ghoul:
        print("Generic Undead")
