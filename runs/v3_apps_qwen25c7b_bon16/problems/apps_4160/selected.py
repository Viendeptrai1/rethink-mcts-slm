import sys

def calculate_years(X):
    balance = 100
    years = 0
    
    while balance < X:
        balance += balance // 100
        years += 1
    
    return years

# Read input
X = int(sys.stdin.read().strip())

# Calculate and print the result
print(calculate_years(X))