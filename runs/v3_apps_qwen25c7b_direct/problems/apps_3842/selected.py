import sys

def min_days_to_dream(p, q, projects):
    # Sort projects by the ratio of money gained to experience gained
    projects.sort(key=lambda x: x[1] / x[0], reverse=True)
    
    total_experience = 0
    total_money = 0
    days = 0
    
    for a_i, b_i in projects:
        if total_experience >= p and total_money >= q:
            break
        
        # Calculate the number of days needed to gain enough experience and money from this project
        remaining_experience_needed = max(0, p - total_experience)
        remaining_money_needed = max(0, q - total_money)
        
        days_needed_for_experience = remaining_experience_needed / a_i
        days_needed_for_money = remaining_money_needed / b_i
        
        # Take the maximum of the two days needed because Mikhail can't work on multiple projects simultaneously
        days_needed = max(days_needed_for_experience, days_needed_for_money)
        
        # Update the total experience and money gained
        total_experience += a_i * days_needed
        total_money += b_i * days_needed
        
        # Add the days worked on this project to the total days
        days += days_needed
    
    return days

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
p = int(data[1])
q = int(data[2])

projects = []
for i in range(n):
    a_i = int(data[3 + 2 * i])
    b_i = int(data[4 + 2 * i])
    projects.append((a_i, b_i))

# Calculate and print the result
result = min_days_to_dream(p, q, projects)
print(f"{result:.10f}")