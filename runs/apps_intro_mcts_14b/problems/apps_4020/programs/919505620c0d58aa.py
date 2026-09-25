import sys

def main():
    import sys
    
    # Read input
    h1, m1 = map(int, sys.stdin.readline().strip().split(':'))
    h2, m2 = map(int, sys.stdin.readline().strip().split(':'))
    
    # Convert start and end times to total minutes since midnight
    start_minutes = h1 * 60 + m1
    end_minutes = h2 * 60 + m2
    
    # Calculate the midpoint in minutes
    midpoint_minutes = (start_minutes + end_minutes) // 2
    
    # Convert the midpoint back to hours and minutes
    h3 = midpoint_minutes // 60
    m3 = midpoint_minutes % 60
    
    # Print the result with leading zeros if necessary
    print(f"{h3:02}:{m3:02}")

if __name__ == "__main__":
    main()