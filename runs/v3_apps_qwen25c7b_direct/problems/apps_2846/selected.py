def h_index(citations):
    citations.sort(reverse=True)
    h = 0
    for i in range(len(citations)):
        if citations[i] >= i + 1:
            h += 1
        else:
            break
    return h

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
citations = list(map(int, data[1:]))

print(h_index(citations))