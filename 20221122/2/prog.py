import sys
t = sys.stdin.buffer.read()
t = t.decode("UTF-8").encode("latin1").decode("cp1251", errors="replace")
sys.stdout.buffer.write(t.encode('utf-8'))