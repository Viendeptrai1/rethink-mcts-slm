import sys

def main():
    x = float(sys.stdin.read().strip())
    scaled_value = int(x * 10)
    
    # Ensure the values are between 1 and 10
    first_integer = min(max(1, scaled_value // 5), 10)
    second_integer = min(max(1, scaled_value % 5 + 1), 10)
    
    print(first_integer, second_integer)

if __name__ == "__main__":
    main()