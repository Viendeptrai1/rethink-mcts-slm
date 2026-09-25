import sys

def max_days(a, b, c):
    # Calculate the maximum number of days the cat can eat without additional food purchases
    # by simulating the consumption pattern from each possible starting day of the week.
    
    # Days of the week and their corresponding food requirements
    days = [
        (3, a),  # Monday, Thursday, Sunday
        (2, b),  # Tuesday, Saturday
        (2, c)   # Wednesday, Friday
    ]
    
    max_days = 0
    
    # Simulate starting from each day of the week
    for i in range(3):
        remaining_fish = a
        remaining_rabbit = b
        remaining_chicken = c
        days_passed = 0
        
        while True:
            # Check if we can continue the trip
            if (i == 0 and remaining_fish >= 3) or \
               (i == 1 and remaining_rabbit >= 2) or \
               (i == 2 and remaining_chicken >= 2):
                if i == 0:
                    remaining_fish -= 3
                elif i == 1:
                    remaining_rabbit -= 2
                else:
                    remaining_chicken -= 2
                days_passed += 1
            else:
                break
            
            # Move to the next day's food requirement
            i = (i + 1) % 3
        
        max_days = max(max_days, days_passed)
    
    return max_days

# Read input
input = sys.stdin.read().split()
a = int(input[0])
b = int(input[1])
c = int(input[2])

# Calculate and print the result
result = max_days(a, b, c)
print(result)