inp = input().split()
W, H, a, b = int(inp[0]), int(inp[1]), float(inp[2]), float(inp[3])
f = inp[4]

eps = 0.05
x = a
res = []
X = []
Y = []

while (x < b):
    X.append(x)
    Y.append(eval(f))
    x += eps

field = [[0] * W for i in range(H)]
minY = min(Y)
maxY = max(Y)
minX = min(X)
maxX = max(X)

for i in range(len(X)):
    x = X[i]
    y = Y[i]
    y_kek = (y - minY) / (maxY - minY) * (H - 1)
    x_kek = (x - minX) / (maxX - minX) * (W - 1)
    field[H - round(y_kek) - 1][round(x_kek)] = 1

for line in field:
    for sym in line:
        if sym == 1:
            print("*", end = '')
        else:
            print(" ", end = '')
    print()
