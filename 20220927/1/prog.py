
a,b = eval(input())

print([num for num in range(a,b) if all(num%i!=0 for i in range(2,num))])
