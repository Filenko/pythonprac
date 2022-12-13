import sys


data = sys.stdin.buffer.read()
n, data, L, f = data[0], data[1:], len(data[1:]), data[0:1]

parts = sorted([data[round(i*L/n):round((i+1)*L/n)] for i in range(n) if data[round(i*L/n):round((i+1)*L/n)]])

sys.stdout.buffer.write(f + b''.join(parts))

