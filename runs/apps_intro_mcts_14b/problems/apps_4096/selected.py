import sys

def min_days_to_finish_coursework(n, m, a):
    # Sort the coffee cups by caffeine content in descending order
    a.sort(reverse=True)
    
    # Initialize variables
    total_pages_written = 0
    days = 0
    
    # Iterate over the sorted list of coffee cups
    for i in range(n):
        # Calculate the number of pages that can be written with the current cup
        pages_today = max(0, a[i] - i)
        total_pages_written += pages_today
        
        # If the total pages written is enough, return the number of days
        if total_pages_written >= m:
            return days + 1
        
        # Increment the day count
        days += 1
    
    # If we exit the loop without writing enough pages, return -1
    return -1

# Read input from standard input
input = sys.stdin.read
data = input().split()

# Parse the input values
n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:]))

# Call the function and print the result
result = min_days_to_finish_coursework(n, m, a)
print(result)