import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    p = [0] * (n + 1)
    for i in range(n):
        p[i+1] = int(input_data[i+1])
    
    visited = [False] * (n + 1)
    q = [0] * (n + 1)
    
    for i in range(1, n + 1):
        if visited[i]:
            continue
        
        # Trace the cycle in p starting from i
        cycle_nodes = []
        curr = i
        while not visited[curr]:
            visited[curr] = True
            cycle_nodes.append(curr)
            curr = p[curr]
        
        cycle_len = len(cycle_nodes)
        
        # If cycle length is odd, we can construct the square root within this cycle
        # If even, we need to pair two cycles of same length, so we can't resolve it alone
        if cycle_len % 2 == 1:
            mid = cycle_len // 2
            for k in range(cycle_len):
                idx = cycle_nodes[k]
                # q[q[idx]] = p[idx]
                # In the cycle decomposition for square root of odd length cycle:
                # Let the cycle be c0 -> c1 -> ... -> c_{L-1} -> c0
                # Then q maps c_k -> c_{k + L//2 mod L}
                # Because applying q twice adds L//2 twice = L = 0 mod L
                # Wait, let's re-verify:
                # We want q[q[x]] = p[x]
                # If q maps c_i -> c_{i+s}, then q[q[c_i]] = c_{i+2s}
                # We want i+2s = i+1 (mod L) => 2s = 1 (mod L)
                # Since L is odd, 2 has an inverse. s = (L+1)//2
                # Let's check: 2 * ((L+1)//2) = L+1 = 1 mod L. Correct.
                
                s = (cycle_len + 1) // 2
                target_idx = (k + s) % cycle_len
                u = cycle_nodes[k]
                v = cycle_nodes[target_idx]
                q[u] = v
        else:
            # Even length cycle cannot be resolved by itself.
            # We must merge two cycles of same length to form one larger cycle of even length
            # which can be split into two odd cycles? No.
            # Actually, squaring an even length cycle produces two cycles of half length.
            # So if we have a cycle of length 2k in q, squaring it gives two cycles of length k in p.
            # Therefore, if we encounter an even length cycle in p, it means the original q had two cycles
            # of that length merged? No, squaring splits.
            # If q has a cycle of length L, p has cycles of length L/gcd(2, L).
            # If L is odd, gcd(2, L)=1, so p has one cycle of length L.
            # If L is even, gcd(2, L)=2, so p has two cycles of length L/2.
            # Thus, if we see a cycle of even length L in p, it must come from a cycle of length 2L in q?
            # No. If q has cycle of length 2L, p has two cycles of length L.
            # So if we have a cycle of length L (even) in p, it implies there is another cycle of length L in p
            # that came from the same cycle in q.
            # We need to find another cycle of the same length to pair with.
            pass

    # We need a different approach: collect all cycles first.
    # Then try to pair even length cycles.
    
    visited = [False] * (n + 1)
    cycles = []
    
    for i in range(1, n + 1):
        if visited[i]:
            continue
        curr = i
        cycle = []
        while not visited[curr]:
            visited[curr] = True
            cycle.append(curr)
            curr = p[curr]
        cycles.append(cycle)
    
    # Group cycles by length
    from collections import defaultdict
    cycles_by_len = defaultdict(list)
    for cyc in cycles:
        cycles_by_len[len(cyc)].append(cyc)
    
    q = [0] * (n + 1)
    
    # Process odd length cycles
    for length, cyc_list in cycles_by_len.items():
        if length % 2 == 1:
            for cyc in cyc_list:
                s = (length + 1) // 2
                for k in range(length):
                    u = cyc[k]
                    v = cyc[(k + s) % length]
                    q[u] = v
        else:
            # Even length cycles must be paired
            if len(cyc_list) % 2 != 0:
                print("-1")
                return
            for i in range(0, len(cyc_list), 2):
                cyc1 = cyc_list[i]
                cyc2 = cyc_list[i+1]
                # We have two cycles of length L: C1 and C2.
                # We want to construct a cycle C of length 2L in q such that C^2 splits into C1 and C2.
                # Structure of C: x0 -> x1 -> ... -> x_{2L-1} -> x0
                # q(x_k) = x_{k+1}
                # q(q(x_k)) = x_{k+2}
                # We want q^2 to map elements of C1 to C1 in order, and C2 to C2 in order.
                # Let C1 = [c0, c1, ..., c_{L-1}] where p(c_i) = c_{i+1} (mod L)
                # Let C2 = [d0, d1, ..., d_{L-1}] where p(d_i) = d_{i+1} (mod L)
                # We set q(c_i) = d_i and q(d_i) = c_{i+1}
                # Check: q[q(c_i)] = q(d_i) = c_{i+1} = p(c_i). Correct.
                # Check: q[q(d_i)] = q(c_{i+1}) = d_{i+1} = p(d_i). Correct.
                
                for k in range(length):
                    q[cyc1[k]] = cyc2[k]
                    q[cyc2[k]] = cyc1[(k+1) % length]
    
    # Output result
    print(*(q[1:]))

if __name__ == "__main__":
    solve()