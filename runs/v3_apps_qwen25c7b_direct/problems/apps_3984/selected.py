def determine_winner(s):
    n = len(s)
    result = []
    
    for k in range(n):
        l, r = k, k
        while True:
            found = False
            for i in range(l - 1, -1, -1):
                for j in range(r + 1, n):
                    if s[i:j] < s[l:r]:
                        l, r = i, j
                        found = True
                        break
                if found:
                    break
            if not found:
                break
        
        if (l, r) == (k, k):
            result.append("Mike")
        else:
            result.append("Ann")
    
    return result

# Example usage:
# s = input().strip()
# print('\n'.join(determine_winner(s)))