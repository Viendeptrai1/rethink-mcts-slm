import sys

def generate_string(n, s, t):
    # Create a list with n 'a's, n 'b's, and n 'c's
    res = ['a'] * n + ['b'] * n + ['c'] * n
    
    # Function to check if a substring exists in the result
    def contains_substring(sub):
        return ''.join(res).find(sub) != -1
    
    # Try to rearrange the characters to avoid s and t
    for i in range(3 * n - 1):
        if contains_substring(s) or contains_substring(t):
            # Swap the current character with the next one
            res[i], res[i + 1] = res[i + 1], res[i]
    
    # Check again if s or t is still in the result
    if contains_substring(s) or contains_substring(t):
        return "NO"
    
    return "YES", ''.join(res)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    result = generate_string(n, s, t)
    if result == "NO":
        print("NO")
    else:
        print("YES")
        print(result[1])

if __name__ == "__main__":
    main()