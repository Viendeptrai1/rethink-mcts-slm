import sys

def main():
    import sys
    a, b, c, d = map(int, sys.stdin.read().split())
    
    # The maximum product will be the product of the largest numbers in the range
    # because multiplying two negative numbers results in a positive number which could be larger
    max_product = max(a * c, a * d, b * c, b * d)
    
    print(max_product)

if __name__ == "__main__":
    main()