x = int(input())
print(f"A {'+' if x % 50 == 0 else '-'} B {'+' if x % 25 == 0 and x % 2 != 0 else '-'} C {'+' if x % 8 == 0 else '-'}")
