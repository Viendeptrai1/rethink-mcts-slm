import sys

def solve():
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()
    
    s_sorted = sorted(s)
    t_sorted = sorted(t, reverse=True)
    
    s_min = "".join(s_sorted)
    t_max = "".join(t_sorted)
    
    if s_min < t_max:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()