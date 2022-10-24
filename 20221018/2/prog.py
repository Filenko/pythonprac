from math import *
i = 0
fns = {}
fns["quit"] = ["fstr", "fstr.format(i, len(fns))"]
while s := input():
    i += 1
    if s[0] == ':':
        t = s.split()
        fns[t[0][1:]] = t[1:]
    else:
        t = s.split()
        local_vars = {}
        for var in zip(fns[t[0]][:-1], t[1:]):
            local_vars[var[0]] = eval(var[1]) if var[1].isnumeric() else var[1]
        #print(fns[t[0]][-1],local_vars)
        print(eval(fns[t[0]][-1],None,local_vars))
    
    


