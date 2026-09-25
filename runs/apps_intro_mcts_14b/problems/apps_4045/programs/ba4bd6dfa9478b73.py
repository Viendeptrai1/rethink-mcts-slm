import sys

def construct_string(n, s, t):
    # Initialize the result string with n 'a's, n 'b's, and n 'c's
    res = ['a'] * n + ['b'] * n + ['c'] * n
    
    # Function to check if adding a character at position i would create s or t
    def is_invalid(i, char):
        if i >= 1 and res[i-1] + char == s:
            return True
        if i >= 1 and res[i-1] + char == t:
            return True
        if i >= 2 and res[i-2] + res[i-1] + char == s + res[i-1]:
            return True
        if i >= 2 and res[i-2] + res[i-1] + char == t + res[i-1]:
            return True
        return False
    
    # Try to rearrange the characters to avoid s and t
    for i in range(3 * n):
        if is_invalid(i, res[i]):
            # Find a valid character to replace res[i]
            for j in range(3 * n):
                if j != i and not is_invalid(i, res[j]):
                    res[i], res[j] = res[j], res[i]
                    break
            else:
                # If no valid replacement found, return "NO"
                return "NO"
    
    return "YES", ''.join(res)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    result, res = construct_string(n, s, t)
    print(result)
    if result == "YES":
        print(res)

if __name__ == "__main__":
    main()