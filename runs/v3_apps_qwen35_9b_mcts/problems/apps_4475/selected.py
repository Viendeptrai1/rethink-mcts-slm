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
        
        # Calculate maximum possible reduction for a and b
        da_max = a - x
        db_max = b - y
        
        # Strategy: Try to reduce the larger number first to minimize product
        # But we need to check both orders or use a direct formula.
        # Actually, since we want to minimize a*b, and the function is convex,
        # we should greedily reduce the larger of the two current values.
        # However, a simpler approach is to try two main strategies:
        # 1. Reduce a as much as possible, then reduce b with remaining n.
        # 2. Reduce b as much as possible, then reduce a with remaining n.
        # Then take the minimum of these two outcomes.
        # Why only these two? Because the optimal solution will always push one variable
        # to its lower bound (x or y) before touching the other, unless n is small enough
        # that we just reduce the larger one. But even in the "small n" case, reducing
        # the larger one is equivalent to one of the two strategies if we consider the
        # order of operations. Specifically:
        # If we reduce a by da and b by db (da+db <= n), the product is (a-da)*(b-db).
        # To minimize this, we want to maximize the reduction of the larger factor.
        # The extreme cases are:
        # Case 1: Maximize reduction of a first.
        # Case 2: Maximize reduction of b first.
        # Any intermediate split where neither is maxed out can be improved by shifting
        # reduction to the larger remaining factor.
        
        # Strategy 1: Reduce a as much as possible
        da1 = min(n, da_max)
        rem_n1 = n - da1
        db1 = min(rem_n1, db_max)
        res1 = (a - da1) * (b - db1)
        
        # Strategy 2: Reduce b as much as possible
        db2 = min(n, db_max)
        rem_n2 = n - db2
        da2 = min(rem_n2, da_max)
        res2 = (a - da2) * (b - db2)
        
        results.append(min(res1, res2))
    
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()