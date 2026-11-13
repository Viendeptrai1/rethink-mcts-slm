def h_index(citations):
    citations.sort(reverse=True)
    h = 0
    for i, c in enumerate(citations):
        if c >= i + 1:
            h = i + 1
        else:
            break
    return h

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
citations = [int(data[i+1]) for i in range(n)]
print(h_index(citations))