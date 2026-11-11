import sys

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, r, avg = read_ints()
    exams = [read_ints() for _ in range(n)]
    
    total_points_needed = n * avg
    current_total_points = sum(a for a, b in exams)
    additional_points_needed = max(0, total_points_needed - current_total_points)
    
    if additional_points_needed == 0:
        print(0)
        return
    
    # Min-heap based on the cost per point (b_i)
    min_heap = []
    for a, b in exams:
        if a < r:
            heapq.heappush(min_heap, (b, a))
    
    essays_needed = 0
    while additional_points_needed > 0 and min_heap:
        b, a = heapq.heappop(min_heap)
        points_to_gain = min(r - a, additional_points_needed)
        essays_needed += points_to_gain * b
        additional_points_needed -= points_to_gain
    
    if additional_points_needed > 0:
        print(-1)
    else:
        print(essays_needed)

if __name__ == "__main__":
    main()