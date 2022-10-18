s = input().lower()
ans = set()

for i in range(len(s)-1):
    if s[i].isalpha() and s[i+1].isalpha(): 
        ans.add(s[i]+s[i+1])

print(len(ans))
