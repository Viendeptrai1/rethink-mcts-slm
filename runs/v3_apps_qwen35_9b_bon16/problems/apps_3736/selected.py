import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    # Map of symmetric characters for the specified font
    # A, H, I, M, O, T, U, V, W, X, Y are symmetric
    # Note: J, K, L, N, P, Q, R, S, Z are not symmetric
    # B, C, D, E, F, G are not symmetric
    symmetric_chars = set('AHIMOTUVWXY')
    
    # Check if all characters are symmetric
    for char in s:
        if char not in symmetric_chars:
            print("NO")
            return
    
    # Now check if the string is a palindrome when reversed
    # Because if we put it in a mirror, the leftmost becomes rightmost and vice versa
    # For the reflection to match the original, the string must be a palindrome
    # AND consist only of symmetric characters (already checked above)
    
    if s == s[::-1]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()