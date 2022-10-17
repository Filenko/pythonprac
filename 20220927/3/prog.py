m1 = []
m2 = []
t = list(eval(input()))
m1.append(t)
for i in range(1,len(m1[0])):
    t = list(eval(input()))
    m1.append(t)
for i in range(len(m1[0])):
    t = list(eval(input()))
    m2.append(t)

ans = [[0 for i in range(len(m1[0]))] for j in range(len(m1[0]))]

for i in range(len(m1[0])):
    for j in range(len(m1[0])):
        res_tmp = 0
        for k in range(len(m1[0])):
            res_tmp += (m1[i][k]*m2[k][j])
        ans[i][j] = res_tmp

for el in ans:
    print(*el, sep=',')

