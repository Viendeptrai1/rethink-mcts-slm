def calculate_years_to_reach_balance(X):
    balance = 100
    years = 0
    
    while balance < X:
        balance = balance * 1.01
        balance = int(balance)  # Discard the fraction of less than one yen
        years += 1
    
    return years

# Read input from standard input
import sys
input = sys.stdin.read
data = input().strip()
X = int(data)

# Calculate and print the result
result = calculate_years_to_reach_balance(X)
print(result)