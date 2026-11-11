import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    # Check if reversing any substring can make the string lexicographically smaller
    found = False
    for i in range(n):
        for j in range(i + 1, n + 1):
            reversed_substring = s[:i] + s[i:j][::-1] + s[j:]
            if reversed_substring < s:
                found = True
                print("YES")
                print(i + 1, j)
                return
    
    if not found:
        print("NO")

if __name__ == "__main__":
    main()