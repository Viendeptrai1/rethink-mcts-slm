import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))

    a = []
    for _ in range(k):
        a.append(int(next(iterator)))

    # Current list of children, initially 1 to n
    children = list(range(1, n + 1))
    
    # Current leader index in the 'children' list
    # Initially, the first child (index 0) is the leader
    leader_idx = 0

    results = []

    for step in range(k):
        count = a[step]
        
        # The leader counts 'count' people starting from the next person.
        # If leader is at index L, the next person is at (L + 1) % current_len.
        # We need to move 'count' steps forward from there.
        # Effectively, the index to eliminate relative to the current list is:
        # (leader_idx + 1 + count - 1) % current_len = (leader_idx + count) % current_len
        
        current_len = len(children)
        elim_idx = (leader_idx + count) % current_len
        
        eliminated_child = children[elim_idx]
        results.append(str(eliminated_child))
        
        # Remove the eliminated child
        children.pop(elim_idx)
        
        # The next player after the eliminated one becomes the new leader.
        # Since we removed the element at elim_idx, the element that was at elim_idx + 1
        # is now at elim_idx. So the new leader index is elim_idx % new_len.
        if len(children) > 0:
            leader_idx = elim_idx % len(children)
        else:
            leader_idx = 0

    print(" ".join(results))

if __name__ == "__main__":
    solve()