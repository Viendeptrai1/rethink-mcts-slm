import sys

def max_product(a, b, c, d):
    # Calculate the product of the maximum values in each range
    max_product = max(a * c, a * d, b * c, b * d)
    return max_product

if __name__ == "__main__":
    # Read input from standard input
    input_values = sys.stdin.read().strip().split()
    a, b, c, d = map(int, input_values)
    
    # Calculate and print the maximum product
    result = max_product(a, b, c, d)
    print(result)