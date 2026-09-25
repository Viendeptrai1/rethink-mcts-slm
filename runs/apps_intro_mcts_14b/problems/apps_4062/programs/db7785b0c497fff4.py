import sys

def main():
    import sys
    a, b, c, d = map(int, sys.stdin.read().split())
    
    # Calculate the product of the extreme values
    products = [
        a * c,
        a * d,
        b * c,
        b * d
    ]
    
    # Find the maximum product
    max_product = max(products)
    
    # Print the result
    print(max_product)

if __name__ == "__main__":
    main()