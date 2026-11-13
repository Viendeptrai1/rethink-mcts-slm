import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    results = []
    
    for _ in range(t):
        a = int(next(iterator))
        b = int(next(iterator))
        x = int(next(iterator))
        y = int(next(iterator))
        n = int(next(iterator))
        
        # Strategy: Try to reduce 'a' as much as possible first, then 'b'
        # Calculate how much we can reduce 'a'
        can_reduce_a = a - x
        if n >= can_reduce_a:
            a_new = x
            n -= can_reduce_a
            can_reduce_b = b - y
            if n >= can_reduce_b:
                b_new = y
            else:
                b_new = b - n
        else:
            a_new = a - n
            b_new = b
        
        ans1 = a_new * b_new
        
        # Strategy: Try to reduce 'b' as much as possible first, then 'a'
        can_reduce_b = b - y
        if n >= can_reduce_b:
            b_new2 = y
            n -= can_reduce_b
            can_reduce_a = a - x
            if n >= can_reduce_a:
                a_new2 = x
            else:
                a_new2 = a - n
        else:
            b_new2 = b - n
            a_new2 = a
        
        ans2 = a_new2 * b_new2
        
        results.append(min(ans1, ans2))
    
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()