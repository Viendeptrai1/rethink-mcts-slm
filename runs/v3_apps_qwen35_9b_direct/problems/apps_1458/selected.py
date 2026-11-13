import sys

def solve():
    n = int(sys.stdin.readline())
    s = sys.stdin.readline().strip()
    
    # We need to find a substring s[l:r+1] (1-based indices l, r) such that
    # reversing it makes the new string lexicographically smaller.
    #
    # Strategy:
    # Find the first index i where s[i] > s[i+1].
    # If we reverse the substring from i to i+1 (just these two characters),
    # the character at position i becomes s[i+1] which is smaller than s[i].
    # Since all previous characters are unchanged, the new string will be lexicographically smaller.
    #
    # If no such i exists, the string is non-decreasing (sorted), and reversing any substring
    # will either keep it same or make it larger at the first differing position.
    # Thus, output NO.
    
    for i in range(n - 1):
        if s[i] > s[i+1]:
            print("YES")
            # Convert 0-based index i to 1-based: l = i+1, r = i+2
            print(f"{i+1} {i+2}")
            return
    
    print("NO")

if __name__ == "__main__":
    solve()