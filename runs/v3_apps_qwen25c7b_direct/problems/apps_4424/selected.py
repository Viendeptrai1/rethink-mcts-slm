import sys

def check_coins(K, X):
    total_value = K * 500
    if total_value >= X:
        return "Yes"
    else:
        return "No"

# Read input from standard input
input_line = sys.stdin.readline().strip()
K, X = map(int, input_line.split())

# Call the function and print the result
print(check_coins(K, X))