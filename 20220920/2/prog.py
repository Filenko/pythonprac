ans = 0
while ans < 21:
    t = int(input())
    if t == 0 or t < 0:
        print(t)
        break
    ans += t
else:
    print(ans)
