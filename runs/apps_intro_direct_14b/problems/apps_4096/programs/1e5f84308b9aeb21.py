import sys
from typing import List

def min_days_to_complete_coursework(n: int, m: int, a: List[int]) -> int:
    # Sort the caffeine levels in descending order
    a.sort(reverse=True)
    
    # Initialize variables
    total_pages_written = 0
    days = 0
    
    # Iterate over the sorted caffeine levels
    for i in range(n):
        # Calculate the number of pages Polycarp can write on this day
        pages_today = max(0, a[i] - i)
        
        # Add the pages written today to the total
        total_pages_written += pages_today
        
        # Increment the day count
        days += 1
        
        # Check if the coursework is completed
        if total_pages_written >= m:
            return days
    
    # If we exit the loop, it means it's impossible to complete the coursework
    return -1

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