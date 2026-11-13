import heapq
from typing import List

def min_days_to_pass_exams(n: int, m: int, d: List[int], a: List[int]) -> int:
    pq = []
    total_days = 0
    
    for i in range(n):
        if d[i] != 0:
            heapq.heappush(pq, (a[d[i]-1], i))
        
        if pq:
            prep_days, exam_day = heapq.heappop(pq)
            if prep_days > total_days:
                return -1
            total_days += 1
        
        if pq:
            total_days += 1
    
    return total_days

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    d = list(map(int, data[2:n+2]))
    a = list(map(int, data[n+2:]))
    
    result = min_days_to_pass_exams(n, m, d, a)
    print(result)