import sys
import heapq

def minimum_days_to_pass_exams(n, m, days, preparation_times):
    # Priority queue to store available subjects sorted by earliest end of preparation
    available_subjects = []
    # Current day in the exam period
    current_day = 0
    # Total days required to pass all exams
    days_passed = 0
    # Set to keep track of passed exams
    passed_exams = set()

    # Iterate over each day in the exam period
    for day in range(n):
        # If there's an exam today, add it to the available subjects
        if days[day] != 0:
            subject = days[day] - 1
            # Calculate when preparation for this subject will end
            end_day = day + preparation_times[subject]
            # Push the preparation end day and subject into the priority queue
            heapq.heappush(available_subjects, (end_day, subject))

        # Try to pass exams if possible
        while available_subjects and current_day <= day:
            end_day, subject = heapq.heappop(available_subjects)
            # Check if this exam can be passed on or before the current day
            if subject not in passed_exams and end_day >= current_day:
                passed_exams.add(subject)
                current_day = end_day  # Move to the end of this preparation period
                days_passed = max(days_passed, current_day)

        # If all exams have been passed, return the number of days passed
        if len(passed_exams) == m:
            return days_passed + 1

    # If we finish the loop and haven't passed all exams, it's impossible
    return -1

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    days = list(map(int, data[2:n+2]))
    preparation_times = list(map(int, data[n+2:n+2+m]))
    
    result = minimum_days_to_pass_exams(n, m, days, preparation_times)
    print(result)

if __name__ == "__main__":
    main()