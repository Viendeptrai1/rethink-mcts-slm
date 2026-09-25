import sys

def is_diverse(s):
    sorted_s = ''.join(sorted(s))
    for i in range(1, len(sorted_s)):
        if ord(sorted_s[i]) != ord(sorted_s[i - 1]) + 1:
            return False
    return True

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    results = []
    
    for i in range(1, n + 1):
        s = data[i]
        if is_diverse(s):
            results.append("Yes")
        else:
            results.append("No")
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()