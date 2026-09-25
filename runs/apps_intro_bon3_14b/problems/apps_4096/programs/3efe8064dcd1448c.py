import sys
from typing import List

def min_days_to_complete_coursework(n: int, m: int, a: List[int]) -> int:
    # Sort the caffeine dosages in descending order
    a.sort(reverse=True)
    
    # Initialize the total pages written and the number of days
    total_pages_written = 0
    days = 0
    
    # Iterate over the sorted list of caffeine dosages
    for i in range(n):
        # Calculate the pages written on the current day
        pages_written_today = max(0, a[i] - i)
        total_pages_written += pages_written_today
        
        # If the total pages written is enough, return the number of days
        if total_pages_written >= m:
            return days + 1
        
        # Increment the day count
        days += 1
    
    # If we finish the loop and still haven't written enough pages, return -1
    return -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:]))
    
    result = min_days_to_complete_coursework(n, m, a)
    print(result)

if __name__ == "__main__":
    main()