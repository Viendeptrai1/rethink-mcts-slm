def rev(num):
    return int(str(num)[::-1])

def count_appearances(A, B):
    count = 0
    current = A
    while current <= B:
        count += 1
        current += rev(current)
    return count

Q = int(input())
results = []
for _ in range(Q):
    A, B = map(int, input().split())
    results.append(count_appearances(A, B))

for result in results:
    print(result)