import heapq
from typing import List

def min_days_to_pass_exams(n: int, m: int, daily_exams: List[int], preparation_days: List[int]) -> int:
    if sum(preparation_days) > n:
        return -1
    
    pq = []
    total_days = 0
    current_day = 0
    
    for day in range(n):
        if daily_exams[day] != 0:
            heapq.heappush(pq, (-preparation_days[daily_exams[day]-1], daily_exams[day]))
        
        if pq:
            _, subject = heapq.heappop(pq)
            total_days += preparation_days[subject-1]
            current_day += preparation_days[subject-1]
        
        if current_day < day + 1:
            total_days += 1
            current_day += 1
    
    return total_days

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    daily_exams = list(map(int, data[2:n+2]))
    preparation_days = list(map(int, data[n+2:]))
    
    result = min_days_to_pass_exams(n, m, daily_exams, preparation_days)
    print(result)