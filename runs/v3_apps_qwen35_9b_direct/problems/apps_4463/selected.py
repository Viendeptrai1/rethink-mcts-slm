import sys

def solve():
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()
    
    # To maximize the chance of s' < t', we should:
    # 1. Sort s in ascending order to make s' as small as possible.
    # 2. Sort t in descending order to make t' as large as possible.
    # If s_sorted < t_sorted_desc, then it's possible.
    
    s_sorted = sorted(s)
    t_sorted_desc = sorted(t, reverse=True)
    
    s_str = ''.join(s_sorted)
    t_str = ''.join(t_sorted_desc)
    
    if s_str < t_str:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()