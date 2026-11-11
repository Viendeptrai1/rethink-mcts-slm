def reverse_number(n):
    return int(str(n)[::-1])

def count_appearances(A, B):
    count = 0
    for i in range(1, B + 1):
        current = i
        while current <= B:
            if A <= current <= B:
                count += 1
            current += reverse_number(current)
    return count

import sys
input = sys.stdin.read
data = input().split()

Q = int(data[0])
queries = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(Q)]

results = [count_appearances(A, B) for A, B in queries]

for result in results:
    print(result)