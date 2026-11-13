import sys

def solve():
    n = int(sys.stdin.readline())
    s = list(sys.stdin.readline().strip())

    # We need to find the first index i where s[i] > s[i+1]
    # Reversing the substring from i+1 to i+2 (1-based: l=i+2, r=i+1+1) might work,
    # but the general strategy is to find the longest non-decreasing prefix.
    # Once we find the first descent s[i] > s[i+1], we can reverse the substring s[i]...s[i+1].
    # However, simply reversing two adjacent characters where s[i] > s[i+1] is sufficient to make the string lexicographically smaller.
    # Why? Because at the first position where the new string differs from the old one,
    # the new string will have s[i+1] and the old will have s[i], and since s[i] > s[i+1], the new is smaller.
    
    # Let's find the first index i (0-based) such that s[i] > s[i+1].
    for i in range(n - 1):
        if s[i] > s[i+1]:
            # Found a descent. Reversing the substring from i to i+1 (length 2) swaps them.
            # Since s[i] > s[i+1], swapping makes s[i] smaller, thus the whole string is lexicographically smaller.
            print("YES")
            # Output 1-based indices
            print(i + 1, i + 2)
            return

    # If no such descent is found, the string is sorted non-decreasingly (e.g., "aabc"),
    # and reversing any substring will result in a string that is lexicographically greater or equal.
    print("NO")

if __name__ == "__main__":
    solve()