import sys
from typing import List

def min_days_to_complete_coursework(n: int, m: int, a: List[int]) -> int:
    # Sort the coffee cups in descending order of caffeine content
    a.sort(reverse=True)
    
    # Initialize the number of days to 0
    days = 0
    
    # While there are still pages left to write
    while m > 0:
        # Increment the day count
        days += 1
        # Initialize the total pages written on this day
        total_pages_today = 0
        
        # Iterate over the coffee cups
        for i in range(n):
            # Calculate the effective pages that can be written with the current cup
            effective_pages = max(0, a[i] - days + 1)
            # Add the effective pages to the total pages written today
            total_pages_today += effective_pages
            # Subtract the effective pages from the total pages left to write
            m -= effective_pages
            # If all pages are written, break out of the loop
            if m <= 0:
                break
        
        # If no pages were written on this day, it's impossible to complete the coursework
        if total_pages_today == 0:
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