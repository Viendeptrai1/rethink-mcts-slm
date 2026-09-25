import sys

def max_days(a, b, c):
    # Calculate the maximum number of days the cat can eat without additional food purchases
    # by considering the optimal starting day of the week.
    
    # Days of the week and their corresponding food requirements
    days = {
        'Monday': [a, 0, 0, b, 0, c, 0],
        'Tuesday': [0, a, 0, 0, b, 0, c],
        'Wednesday': [0, 0, a, 0, b, 0, c],
        'Thursday': [a, 0, 0, b, 0, c, 0],
        'Friday': [0, a, 0, 0, b, 0, c],
        'Saturday': [0, 0, a, b, 0, c, 0],
        'Sunday': [a, 0, 0, b, 0, c, 0]
    }
    
    max_days = 0
    
    for start_day, food_requirements in days.items():
        # Calculate the number of full weeks the cat can survive
        full_weeks = min(food // req for food, req in zip([a, b, c], food_requirements))
        
        # Calculate the remaining food after full weeks
        remaining_food = [food - full_weeks * req for food, req in zip([a, b, c], food_requirements)]
        
        # Calculate the number of additional days the cat can survive with the remaining food
        additional_days = 0
        for i in range(7):
            if remaining_food[i % 3] > 0:
                additional_days += 1
                remaining_food[i % 3] -= 1
        
        # Total days the cat can survive starting from this day
        total_days = full_weeks * 7 + additional_days
        
        # Update the maximum number of days
        max_days = max(max_days, total_days)
    
    return max_days

# Read input
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])
c = int(data[2])

# Calculate and print the result
result = max_days(a, b, c)
print(result)