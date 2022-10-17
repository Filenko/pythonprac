def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s

n = int(input())

for i in (n,n+1,n+2):
    for j in (n,n+1,n+2):
        f = i * j
        print(i,' * ',j, ' = ', f if sum_digits(f) != 6 else ':=)', end=' ')
    print("")



        
