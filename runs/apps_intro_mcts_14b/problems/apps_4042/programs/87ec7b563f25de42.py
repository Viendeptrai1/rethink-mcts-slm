import sys

def main():
    x = float(sys.stdin.read().strip())
    
    # Scale x to a range between 1 and 100
    scaled_x = int(x * 100)
    
    # Calculate the two integers
    first_int = min(10, max(1, scaled_x // 10))
    second_int = min(10, max(1, scaled_x % 10))
    
    # Output the result
    print(first_int, second_int)

if __name__ == "__main__":
    main()