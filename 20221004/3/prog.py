def sub(a,b):
	if type(a) == tuple or type(a) == list:
		ans = type(a)()
		for el in a:
			flag = False
			for el1 in b:
				if el == el1:
					flag = True
			if not flag:
				t = type(a)((el,))
				ans += t
		return ans
	else:
		return a - b



a,b = eval(input())
print(sub(a,b))