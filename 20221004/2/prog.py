
def Pareto(*args):
	ans = []
	for (i, el) in enumerate(args):
		flag = False
		for (j,el) in enumerate(args):
			if j != i:
				if (args[i][0] <= args[j][0] and args[i][1] <= args[j][1] 
				and (args[i][0] < args[j][0] or args[i][1] < args[j][1])):
					flag = True
		if not flag:
			ans.append(args[i])
	return ans

t = eval(input())
print(Pareto(*t))


