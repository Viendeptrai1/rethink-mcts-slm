def min_days_to_pass_exams(n, m, days, preparation_days):
    from heapq import heappop, heappush
    import sys

    # Initialize a list to keep track of the earliest day each subject can be passed
    earliest_pass_day = [sys.maxsize] * (m + 1)

    # Priority queue to manage the preparation days
    prep_days_heap = []

    # Iterate over each day
    for day in range(n):
        subject = days[day]

        # If there's an exam on this day, we need to pass it
        if subject != 0:
            # If we have already prepared enough days for this subject, pass it
            if earliest_pass_day[subject] <= day:
                earliest_pass_day[subject] = sys.maxsize
            else:
                # Otherwise, we need to prepare for this subject
                heappush(prep_days_heap, (day + preparation_days[subject - 1], subject))

        # Process the heap to see if we can pass any exams
        while prep_days_heap:
            end_day, subj = heappop(prep_days_heap)
            if earliest_pass_day[subj] == sys.maxsize:
                earliest_pass_day[subj] = end_day
            else:
                # If we can't pass it yet, push it back with updated end day
                heappush(prep_days_heap, (end_day, subj))
                break

    # Check if all subjects have been passed
    max_day = max(earliest_pass_day)
    return max_day if max_day != sys.maxsize else -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
days = list(map(int, data[2:n+2]))
preparation_days = list(map(int, data[n+2:n+2+m]))

# Get the result
result = min_days_to_pass_exams(n, m, days, preparation_days)

# Print the result
print(result)