def rev(num):
    return int(str(num)[::-1])

def count_appearances(A, B):
    count = 0
    for i in range(1, B + 1):
        current = i
        while current <= B:
            if A <= current <= B:
                count += 1
            current += rev(current)
    return count

Q = int(input())
queries = [tuple(map(int, input().split())) for _ in range(Q)]

results = [count_appearances(A, B) for A, B in queries]

for result in results:
    print(result)