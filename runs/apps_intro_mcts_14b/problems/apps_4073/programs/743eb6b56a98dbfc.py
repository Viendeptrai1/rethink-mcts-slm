import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    numbers = list(map(int, sys.stdin.readline().strip().split()))
    
    product = 1
    for num in numbers:
        product *= num
    
    result = product % 10
    print(result)

if __name__ == "__main__":
    main()