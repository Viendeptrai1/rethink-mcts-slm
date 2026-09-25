import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    a = sys.stdin.readline().strip()
    f = list(map(int, sys.stdin.readline().strip().split()))
    
    max_digit = max(f)
    max_index = f.index(max_digit)
    
    max_number = ''.join(str(max_digit) if int(digit) == max_index + 1 else digit for digit in a)
    
    print(max_number)

if __name__ == "__main__":
    main()