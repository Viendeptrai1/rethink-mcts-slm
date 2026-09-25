import sys

def main():
    x = float(sys.stdin.read().strip())
    floored_value = int(x * 100)
    
    if floored_value < 10:
        print(floored_value, 1)
    else:
        first_integer = floored_value // 10
        second_integer = (floored_value % 10) + 1
        print(first_integer, second_integer)

if __name__ == "__main__":
    main()