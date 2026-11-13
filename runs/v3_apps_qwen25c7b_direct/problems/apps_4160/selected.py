import sys

def calculate_years_to_reach_balance(X):
    balance = 100
    years = 0
    
    while balance < X:
        balance += balance // 100
        years += 1
    
    return years

# Read input from stdin
X = int(sys.stdin.read().strip())

# Calculate the number of years
result = calculate_years_to_reach_balance(X)

# Print the result
print(result)