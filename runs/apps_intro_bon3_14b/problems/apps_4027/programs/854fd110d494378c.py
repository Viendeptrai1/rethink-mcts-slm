import sys

def main():
    import sys
    n = int(sys.stdin.read().strip())
    
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 == 0:
        print(0)
    else:
        print(1)

if __name__ == "__main__":
    main()