import sys
from typing import List

def min_days_to_complete_coursework(n: int, m: int, a: List[int]) -> int:
    a.sort(reverse=True)
    total_pages = 0
    days = 0
    
    while total_pages < m:
        days += 1
        pages_written_today = 0
        for i in range(n):
            if a[i] > 0:
                pages_written_today += max(0, a[i] - days + 1)
                a[i] -= 1
                if total_pages + pages_written_today >= m:
                    return days
        total_pages += pages_written_today
        if pages_written_today == 0:
            return -1
    
    return days

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    
    result = min_days_to_complete_coursework(n, m, a)
    print(result)

if __name__ == "__main__":
    main()