import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    a = sys.stdin.readline().strip()
    f = list(map(int, sys.stdin.readline().strip().split()))
    
    max_digit = max(f)
    max_index = f.index(max_digit)
    
    result = []
    for char in a:
        if int(char) == max_index + 1:
            result.append(str(max_digit))
        else:
            result.append(char)
    
    print(''.join(result))

if __name__ == "__main__":
    main()