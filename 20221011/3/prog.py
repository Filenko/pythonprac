import sys
s = sys.stdin.read()
liq_start = s.count("~")
gas_start = s.count(".")

liq = s.count("~")
s = s.split('\n')
a, b = len(s) - 2, len(s[0]) - 2
liq_num = liq // a + (1 if liq % a != 0 else 0)
gas_num = b - liq_num
a, b = b, a
ans = "#" * (b + 2) + "\n" + gas_num * ("#" + b * "." + "#" + "\n")\
      + liq_num * ("#" + b * "~" + "#" + "\n") + "#" * (b + 2)
print(ans)

total = liq_start + gas_start
length = len(str(total) + "/" + str(max(liq_start,gas_start)))

print(("." * round(20 * gas_start / max(gas_start, liq_start))).ljust(20), f"{gas_start}/{total}".rjust(length))
print(("~" * round(20 * liq_start / max(gas_start, liq_start))).ljust(20), f"{liq_start}/{total}".rjust(length))
