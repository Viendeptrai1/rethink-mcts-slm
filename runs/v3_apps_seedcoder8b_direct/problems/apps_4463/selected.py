def can_satisfy_lexicographic_order(s, t):
    # Sort both strings
    s_sorted = sorted(s)
    t_sorted = sorted(t)
    
    # Compare sorted strings
    return ''.join(s_sorted) < ''.join(t_sorted)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    s = data[0]
    t = data[1]
    
    if can_satisfy_lexicographic_order(s, t):
        print("Yes")
    else:
        print("No")