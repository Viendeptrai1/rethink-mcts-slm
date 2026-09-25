import sys

def main():
    x = float(sys.stdin.read().strip())
    
    # Convert the floating-point number to an integer by multiplying by 1000000
    # and then taking the integer part.
    num = int(x * 1000000)
    
    # Calculate the two integers based on the properties of the number.
    first_int = (num // 100000) % 10 + 1
    second_int = (num // 1000) % 10 + 1
    
    # Print the two integers separated by a space.
    print(first_int, second_int)

if __name__ == "__main__":
    main()