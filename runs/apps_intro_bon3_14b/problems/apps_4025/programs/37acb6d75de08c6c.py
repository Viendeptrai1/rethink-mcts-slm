import sys

def max_days(a, b, c):
    # Calculate the maximum number of days the cat can eat without additional food purchases
    # for each possible starting day of the week.
    
    # Days of the week and their corresponding food requirements
    days = [
        (3, a),  # Monday, Thursday, Sunday
        (2, b),  # Tuesday, Saturday
        (2, c)   # Wednesday, Friday
    ]
    
    # Sort days by the number of days in descending order, and by the amount of food in ascending order
    days.sort(key=lambda x: (-x[0], x[1]))
    
    # Initialize the maximum number of days
    max_days = 0
    
    # Iterate over each possible starting day
    for i in range(3):
        # Calculate the total number of days the cat can eat with the current starting day
        total_days = 0
        remaining_food = [a, b, c]
        
        for j in range(3):
            days_in_week = days[j][0]
            food_needed = days[j][1]
            
            # Calculate the number of full weeks the cat can eat with the current food supply
            full_weeks = remaining_food[i] // food_needed
            total_days += full_weeks * days_in_week
            
            # Update the remaining food after eating for the full weeks
            remaining_food[i] -= full_weeks * food_needed
            
            # If there is enough food left for one more day, add one more day
            if remaining_food[i] >= food_needed:
                total_days += 1
                remaining_food[i] -= food_needed
        
        # Update the maximum number of days
        max_days = max(max_days, total_days)
    
    return max_days

# Read input from standard input
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])
c = int(data[2])

# Calculate and print the result
result = max_days(a, b, c)
print(result)