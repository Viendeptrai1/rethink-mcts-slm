import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        a = []
        for _ in range(k):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    # List of children currently in the circle
    children = list(range(1, n + 1))
    
    # Index of the current leader in the `children` list (0-based)
    # Initially, child 1 is the leader, which is at index 0
    leader_idx = 0
    
    results = []
    
    for step in range(k):
        # Count a[step] people starting from the next person after the leader
        # If we count m people starting from next, the person eliminated is at:
        # (leader_idx + m) % current_length
        # Because:
        # - next person is at (leader_idx + 1) % L
        # - 1st counted is at (leader_idx + 1) % L
        # - 2nd counted is at (leader_idx + 2) % L
        # - m-th counted is at (leader_idx + m) % L
        
        current_count = a[step]
        current_length = len(children)
        
        eliminated_idx = (leader_idx + current_count) % current_length
        eliminated_child = children[eliminated_idx]
        
        results.append(str(eliminated_child))
        
        # Remove the eliminated child
        children.pop(eliminated_idx)
        
        # The new leader is the next person after the eliminated one.
        # Since we removed the element at eliminated_idx, the person who was at
        # (eliminated_idx + 1) % current_length is now at index eliminated_idx % new_length.
        if len(children) > 0:
            leader_idx = eliminated_idx % len(children)
        else:
            # Should not happen given constraints (k <= n-1)
            leader_idx = 0

    print(" ".join(results))

if __name__ == "__main__":
    solve()