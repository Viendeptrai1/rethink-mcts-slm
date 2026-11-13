def find_substring_to_reverse(n, s):
    for i in range(n - 1):
        for j in range(i + 1, n):
            # Check if reversing substring s[i:j+1] results in a lexicographically smaller string
            if s[:i] + s[i:j+1][::-1] + s[j+1:] < s:
                return "YES", i + 1, j + 1
    return "NO"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = find_substring_to_reverse(n, s)
    if isinstance(result, tuple):
        print(result[0])
        print(result[1], result[2])
    else:
        print(result)

if __name__ == "__main__":
    main()