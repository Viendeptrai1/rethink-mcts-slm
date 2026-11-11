import sys

def main():
    # Read input from standard input
    input = sys.stdin.read
    data = input().split()
    
    # Convert input strings to integers
    A = int(data[0])
    B = int(data[1])
    
    # Calculate the three possible values
    sum_value = A + B
    diff_value = A - B
    product_value = A * B
    
    # Find the largest value among the three
    largest_value = max(sum_value, diff_value, product_value)
    
    # Print the largest value
    print(largest_value)

if __name__ == "__main__":
    main()