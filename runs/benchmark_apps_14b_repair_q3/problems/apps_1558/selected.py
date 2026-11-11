import sys
import heapq

def main():
    def read_ints():
        return map(int, sys.stdin.readline().split())
    
    n, r, avg = read_ints()
    total_required_score = n * avg
    current_total_score = 0
    max_heap = []
    
    for _ in range(n):
        a_i, b_i = read_ints()
        current_total_score += a_i
        if a_i < r:
            heapq.heappush(max_heap, (b_i, a_i))
    
    if current_total_score >= total_required_score:
        print(0)
        return
    
    additional_score_needed = total_required_score - current_total_score
    essays_needed = 0
    
    while max_heap and additional_score_needed > 0:
        b_i, a_i = heapq.heappop(max_heap)
        possible_increase = min(r - a_i, additional_score_needed)
        additional_score_needed -= possible_increase
        essays_needed += possible_increase * b_i
    
    if additional_score_needed == 0:
        print(essays_needed)
    else:
        print(-1)

if __name__ == "__main__":
    main()