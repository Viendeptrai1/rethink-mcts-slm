import sys

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, r, avg = read_ints()
    total_required = n * avg
    current_total = 0
    max_heap = []
    
    for _ in range(n):
        a_i, b_i = read_ints()
        current_total += a_i
        if a_i < r:
            heapq.heappush(max_heap, (-b_i, a_i))
    
    essays_needed = 0
    
    while current_total < total_required and max_heap:
        b_i, a_i = heapq.heappop(max_heap)
        b_i = -b_i
        increment = min(r - a_i, total_required - current_total)
        current_total += increment
        essays_needed += increment * b_i
    
    if current_total >= total_required:
        print(essays_needed)
    else:
        print(-1)

if __name__ == "__main__":
    main()