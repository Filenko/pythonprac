import sys
import struct

wav_file = sys.stdin.buffer.read(50)

if len(wav_file) < 44:
    print("NO")
    exit(0)
if struct.unpack("4s", wav_file[8:12])[0] != b"WAVE":
    print("NO")
    exit(0)

slices = [[4, 8], [20, 22], [22, 24], [24, 28], [34, 36], [40, 44]]
slice_str = ['i', 'h', 'h', 'i', 'h', 'i']
names_ = ["Size", "Type", "Channels", "Rate", "Bits", "Data size"]
res = []

for i in range(len(slice_str)):
    start, stop = slices[i]
    s = slice_str[i]

    res.append(struct.unpack(s, wav_file[start:stop])[0])

result_str = ""
for i in range(len(slice_str)):
    if i != len(slice_str) - 1:
        print(names_[i] + "=" + str(res[i]), end=', ')
    else:
        print(names_[i] + "=" + str(res[i]))