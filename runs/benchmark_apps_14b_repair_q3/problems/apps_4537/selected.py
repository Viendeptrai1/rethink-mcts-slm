import sys

def main():
    # Read input from standard input
    input = sys.stdin.read().split()
    A = int(input[0])
    B = int(input[1])
    
    # Calculate the three possible values
    sum_value = A + B
    diff_value = A - B
    prod_value = A * B
    
    # Find the largest value among the three
    largest_value = max(sum_value, diff_value, prod_value)
    
    # Print the largest value
    print(largest_value)

if __name__ == "__main__":
    main()