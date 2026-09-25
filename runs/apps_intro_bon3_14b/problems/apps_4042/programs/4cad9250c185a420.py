import sys

def main():
    x = float(sys.stdin.read().strip())
    
    # Convert the floating-point number to an integer by multiplying by 1000000
    # and then taking the integer part.
    x_int = int(x * 1000000)
    
    # Calculate the two integers based on the value of x_int
    a = (x_int // 100000) % 10 + 1
    b = (x_int // 10000) % 10 + 1
    
    # Print the result
    print(a, b)

if __name__ == "__main__":
    main()