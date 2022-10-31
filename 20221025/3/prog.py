from itertools import product

print(*list(map(lambda x : "".join(x), sorted(filter(lambda x : "".join(x).count("TOR")==2,product(["T", "O", "R"], repeat = int(input()))), key = lambda x: "".join(x)))), sep=", ")


