def get_kth_char(n, k):
    if n == 0:
        s = "What are you doing at the end of the world? Are you busy? Will you save us?"
    else:
        s = "What are you doing while sending "
        s += '"' * n + s[:n] + '"' * n + "? Are you busy? Will you send "
        s += '"' * n + s[:n] + '"' * n + "?"
    
    if k <= len(s):
        return s[k-1]
    else:
        return '.'

import sys
input = sys.stdin.read
data = input().split()

q = int(data[0])
results = []

for i in range(1, q*2, 2):
    n = int(data[i])
    k = int(data[i+1])
    results.append(get_kth_char(n, k))

print(''.join(results))