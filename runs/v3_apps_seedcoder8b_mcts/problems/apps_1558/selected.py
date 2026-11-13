import heapq
import sys

def min_essays_to_get_scholarship(n, r, avg, exams):
    current_sum = sum(a for a, b in exams)
    required_sum = avg * n
    if current_sum >= required_sum:
        return 0

    essays_needed = 0
    heap = []

    for a, b in exams:
        if a < r:
            heapq.heappush(heap, (b, a))

    while heap and current_sum < required_sum:
        b, a = heapq.heappop(heap)
        increase = min(r - a, required_sum - current_sum)
        essays_needed += increase * b
        current_sum += increase

    return essays_needed

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    r = int(data[1])
    avg = int(data[2])
    
    exams = []
    index = 3
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        exams.append((a, b))
        index += 2
    
    result = min_essays_to_get_scholarship(n, r, avg, exams)
    print(result)

if __name__ == "__main__":
    main()