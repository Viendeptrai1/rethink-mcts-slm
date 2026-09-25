import sys

def main():
    import sys
    a, b, c, d = map(int, sys.stdin.read().split())
    
    # The maximum product will be the product of the largest absolute values
    # within the given ranges for x and y.
    max_product = max(a * c, a * d, b * c, b * d)
    
    print(max_product)

if __name__ == "__main__":
    main()