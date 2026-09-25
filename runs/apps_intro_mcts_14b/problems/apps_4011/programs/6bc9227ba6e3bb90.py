import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    a = sys.stdin.readline().strip()
    f = list(map(int, sys.stdin.readline().strip().split()))
    
    max_digit = max(f)
    max_index = f.index(max_digit)
    
    result = ''.join(str(max_digit) if int(char) == max_index + 1 else char for char in a)
    
    print(result)

if __name__ == "__main__":
    main()