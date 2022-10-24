import re
import collections
n = int(input())

ans_dict = {}

while s := input():
	words = re.findall(r'\w+', s)
	for word in words:
		if len(word) != n:
			continue
		word = word.lower()
		if word not in ans_dict:
			ans_dict[word] = 0
		ans_dict[word] += 1

od = collections.OrderedDict(sorted(ans_dict.items(), key = lambda x: x[1], reverse=True))
first_item = list(od.items())[0]

wordss = [x[0] for x in od.items() if x[1] == first_item[1]]
print(*sorted(wordss), sep = " ")



