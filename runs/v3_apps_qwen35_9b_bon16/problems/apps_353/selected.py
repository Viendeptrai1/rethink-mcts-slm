import sys

def solve():
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return
        
        n = int(input_data[0])
        a = [int(x) for x in input_data[1:n+1]]
    except Exception:
        return

    if n == 1:
        if a[0] == 0:
            print("UP")
        elif a[0] == 15:
            print("DOWN")
        else:
            print("-1")
        return

    # Check if the sequence is already invalid (not needed per problem guarantee but good for sanity)
    # The cycle is: 0, 1, 2, ..., 15, 14, ..., 1, 0, ...
    # Pattern: increases by 1 until 15, then decreases by 1 to 0.
    
    # Let's reconstruct the possible starting positions in the cycle.
    # The full cycle length is 30.
    cycle = list(range(16)) + list(range(14, -1, -1))
    
    # We need to find all indices i such that cycle[i] == a[0], cycle[i+1] == a[1], ...
    # Since n <= 92 and cycle length is 30, we can just simulate or check matches.
    
    possible_indices = []
    
    # The sequence could start at any index in the infinite repetition of the cycle.
    # However, since the pattern repeats every 30 days, we only need to check indices 0 to 29.
    # But wait, if n > 30, the constraints on the sequence become very strict.
    # Actually, we can just check every position in the first 30 elements of the cycle.
    
    for start_idx in range(30):
        valid = True
        for j in range(n):
            idx = (start_idx + j) % 30
            if cycle[idx] != a[j]:
                valid = False
                break
        if valid:
            possible_indices.append(start_idx)
    
    if len(possible_indices) == 0:
        # This should not happen based on problem statement "guaranteed consistent"
        print("-1")
        return

    # Determine the next value for each possible start index
    next_values = []
    for start_idx in possible_indices:
        next_idx = (start_idx + n) % 30
        next_val = cycle[next_idx]
        current_val = a[-1]
        if next_val < current_val:
            next_values.append("DOWN")
        elif next_val > current_val:
            next_values.append("UP")
        else:
            next_values.append("SAME") # Should not happen in cycle except at boundaries which are handled by < or >
    
    # Collect unique outcomes
    outcomes = set(next_values)
    
    if "DOWN" in outcomes and "UP" not in outcomes:
        print("DOWN")
    elif "UP" in outcomes and "DOWN" not in outcomes:
        print("UP")
    else:
        # Mixed outcomes or impossible to determine
        print("-1")

if __name__ == "__main__":
    solve()