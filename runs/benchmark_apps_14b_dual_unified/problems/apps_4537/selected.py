import sys

def main():
    # Read input from standard input
    input = sys.stdin.read().strip()
    A, B = map(int, input.split())
    
    # Calculate the three possible values
    sum_value = A + B
    diff_value = A - B
    prod_value = A * B
    
    # Find the maximum value among the three
    max_value = max(sum_value, diff_value, prod_value)
    
    # Print the result
    print(max_value)

if __name__ == "__main__":
    main()