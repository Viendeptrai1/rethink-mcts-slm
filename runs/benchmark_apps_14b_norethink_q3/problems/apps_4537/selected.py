import sys

def main():
    # Read input from standard input
    input = sys.stdin.read().strip()
    A, B = map(int, input.split())
    
    # Calculate the three possible results
    sum_result = A + B
    diff_result = A - B
    prod_result = A * B
    
    # Determine the maximum value among the three results
    max_value = max(sum_result, diff_result, prod_result)
    
    # Print the maximum value
    print(max_value)

if __name__ == "__main__":
    main()