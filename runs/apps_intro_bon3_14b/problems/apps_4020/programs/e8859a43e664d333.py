import sys

def calculate_midpoint(h1, m1, h2, m2):
    # Convert start and end times to total minutes since midnight
    start_minutes = h1 * 60 + m1
    end_minutes = h2 * 60 + m2
    
    # Calculate the midpoint in minutes
    midpoint_minutes = (start_minutes + end_minutes) // 2
    
    # Convert back to hours and minutes
    h3 = midpoint_minutes // 60
    m3 = midpoint_minutes % 60
    
    # Format the output as hh:mm
    return f"{h3:02}:{m3:02}"

# Read input from standard input
input = sys.stdin.read().strip().split('\n')
h1, m1 = map(int, input[0].split(':'))
h2, m2 = map(int, input[1].split(':'))

# Calculate and print the midpoint
print(calculate_midpoint(h1, m1, h2, m2))