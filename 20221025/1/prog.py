def fib(m, n):
	f = 1
	s = 1
	fib = 2
	i = 2
	while i != n:
		fib = f + s
		f = s
		s = fib
		i += 1
	for k in range(n):
		yield fib
		fib = f + s
		f = s
		s = fib


print(*fib(4, 5))




