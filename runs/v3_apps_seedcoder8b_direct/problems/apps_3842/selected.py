def min_days_to_dream(n, p, q, projects):
    # Sort projects by the ratio of experience to income in descending order
    projects.sort(key=lambda x: x[0] / x[1], reverse=True)

    # Initialize variables
    experience = 0
    income = 0
    days = 0.0

    # Iterate over sorted projects
    for a_i, b_i in projects:
        if experience >= p and income >= q:
            break

        # Calculate the maximum possible days for the current project
        max_days = float('inf')
        if a_i > 0:
            max_days = (p - experience) / a_i
        if b_i > 0:
            max_days = min(max_days, (q - income) / b_i)

        # Update experience and income
        experience += a_i * max_days
        income += b_i * max_days
        days += max_days

    return days

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
p = int(data[1])
q = int(data[2])
projects = []

index = 3
for _ in range(n):
    a_i = int(data[index])
    b_i = int(data[index + 1])
    projects.append((a_i, b_i))
    index += 2

# Calculate and print the result
result = min_days_to_dream(n, p, q, projects)
print(f"{result:.12f}")