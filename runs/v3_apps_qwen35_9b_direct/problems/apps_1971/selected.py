import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    p = [0] * (n + 1)
    for i in range(1, n + 1):
        p[i] = int(input_data[i])

    visited = [False] * (n + 1)
    q = [0] * (n + 1)

    for i in range(1, n + 1):
        if visited[i]:
            continue

        # Trace the cycle in p starting from i
        cycle = []
        curr = i
        while not visited[curr]:
            visited[curr] = True
            cycle.append(curr)
            curr = p[curr]

        # Check if cycle length is odd
        length = len(cycle)
        if length % 2 == 1:
            # Odd length cycles can be square-rooted by shifting elements
            # q[cycle[k]] = cycle[(k + (length-1)//2) % length]
            shift = (length - 1) // 2
            for k in range(length):
                src = cycle[k]
                dst = cycle[(k + shift) % length]
                q[src] = dst
        else:
            # Even length cycles: we need to pair them up to form a valid square root
            # If there's an odd number of even-length cycles, it's impossible
            # We will collect all even-length cycles and try to pair them
            pass

    # Collect even-length cycles
    even_cycles = []
    for i in range(1, n + 1):
        if visited[i]:
            continue
        cycle = []
        curr = i
        while not visited[curr]:
            visited[curr] = True
            cycle.append(curr)
            curr = p[curr]
        
        if len(cycle) % 2 == 0:
            even_cycles.append(cycle)

    # Check if we have an even number of even-length cycles
    if len(even_cycles) % 2 != 0:
        print("-1")
        return

    # Pair up even-length cycles
    idx = 0
    while idx < len(even_cycles):
        cycle1 = even_cycles[idx]
        cycle2 = even_cycles[idx + 1]
        idx += 2

        len1 = len(cycle1)
        len2 = len(cycle2)

        # We need to interleave the two cycles to form a valid square root
        # Let cycle1 = [a0, a1, ..., a_{m-1}] and cycle2 = [b0, b1, ..., b_{m-1}]
        # We set q[a_i] = b_i and q[b_i] = a_{(i + m/2) % m} ? 
        # Actually, the standard construction is:
        # q[a_i] = b_i
        # q[b_i] = a_{(i + m/2) % m}
        # Then q^2[a_i] = q[b_i] = a_{(i + m/2) % m} -> this doesn't match p[a_i] = a_{i+1}
        
        # Correct construction for two cycles of same length m:
        # Let cycle1 = [c0, c1, ..., c_{m-1}] where p[c_i] = c_{(i+1)%m}
        # Let cycle2 = [d0, d1, ..., d_{m-1}] where p[d_i] = d_{(i+1)%m}
        # We want q such that q^2[c_i] = c_{i+1} and q^2[d_i] = d_{i+1}
        # Set q[c_i] = d_i and q[d_i] = c_{(i + m/2) % m}
        # Then q^2[c_i] = q[d_i] = c_{(i + m/2) % m} -> This is not c_{i+1} unless m/2 = 1 mod m? No.
        
        # Let's re-derive:
        # We need q[q[c_i]] = c_{i+1}
        # Let q[c_i] = d_i. Then q[d_i] must be c_{i+1}.
        # But then q[q[d_i]] = q[c_{i+1}] = d_{i+1}, which matches p[d_i] = d_{i+1}.
        # So the mapping is:
        # q[c_i] = d_i
        # q[d_i] = c_{i+1}
        # This works if the cycles have the same length.
        
        # However, our cycles are just lists of elements. We need to align them so that
        # p[c_i] = c_{next} and p[d_i] = d_{next}.
        # Since cycle1 and cycle2 are extracted by following p, they are already in order.
        # cycle1[k] -> p[cycle1[k]] = cycle1[(k+1)%len1]
        # cycle2[k] -> p[cycle2[k]] = cycle2[(k+1)%len2]
        
        # So we can set:
        # q[cycle1[k]] = cycle2[k]
        # q[cycle2[k]] = cycle1[(k+1) % len1]
        
        # Let's verify:
        # q^2[cycle1[k]] = q[cycle2[k]] = cycle1[(k+1)%len1] = p[cycle1[k]] -> Correct.
        # q^2[cycle2[k]] = q[cycle1[(k+1)%len1]] = cycle2[(k+1)%len2] = p[cycle2[k]] -> Correct.
        
        m = len1  # len1 == len2
        for k in range(m):
            q[cycle1[k]] = cycle2[k]
            q[cycle2[k]] = cycle1[(k + 1) % m]

    # Output result
    result = []
    for i in range(1, n + 1):
        result.append(str(q[i]))
    print(" ".join(result))

if __name__ == "__main__":
    solve()