import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    total_sum = sum(a)
    result = total_sum % 10
    
    print(result)

if __name__ == "__main__":
    main()