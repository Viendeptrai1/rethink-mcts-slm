import sys

def main():
    import sys
    import sys
    import sys
    
    n = int(sys.stdin.readline().strip())
    a = sys.stdin.readline().strip()
    f = list(map(int, sys.stdin.readline().strip().split()))
    
    max_digit = max(f)
    max_index = f.index(max_digit)
    
    max_number = ""
    found = False
    
    for i in range(n):
        if int(a[i]) == max_index + 1:
            found = True
        if found:
            max_number += str(max_digit)
        else:
            max_number += a[i]
    
    print(max_number)

if __name__ == "__main__":
    main()