import sys
from collections import deque

def min_days_to_pass_exams(n, m, days, preparation_days):
    # Initialize the earliest day each subject can be passed
    earliest_pass_day = [float('inf')] * (m + 1)
    
    # Queue to manage the preparation days
    preparation_queue = deque()
    
    # Iterate over each day
    for day in range(n):
        subject = days[day]
        
        # If there's an exam on this day, update the earliest pass day
        if subject != 0:
            earliest_pass_day[subject] = min(earliest_pass_day[subject], day + preparation_days[subject - 1])
        
        # Add the current day to the preparation queue
        preparation_queue.append(day)
        
        # Remove days from the queue that are no longer relevant
        while preparation_queue and preparation_queue[0] < day - max(preparation_days) + 1:
            preparation_queue.popleft()
        
        # Check if we can pass all exams with the current preparation window
        if all(day >= earliest_pass_day[i] for i in range(1, m + 1)):
            return day + 1
    
    # If we exit the loop without passing all exams, it's impossible
    return -1

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    days = list(map(int, data[2:n + 2]))
    preparation_days = list(map(int, data[n + 2:n + 2 + m]))
    
    result = min_days_to_pass_exams(n, m, days, preparation_days)
    print(result)

if __name__ == "__main__":
    main()