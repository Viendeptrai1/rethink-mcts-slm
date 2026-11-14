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

    children = list(range(1, n + 1))
    leader_idx = 0  # Index of the current leader in the children list

    results = []

    for count in a:
        # The leader counts 'count' people starting from the next person.
        # This means we move 'count' steps forward from the leader's current position.
        # Since the list is circular, we use modulo arithmetic.
        elim_idx = (leader_idx + count) % len(children)
        
        # The child at elim_idx is eliminated
        eliminated_child = children.pop(elim_idx)
        results.append(eliminated_child)
        
        # The new leader is the person who was immediately after the eliminated one.
        # In the new list (after pop), the person who was at elim_idx + 1 (or wrapped)
        # is now at index elim_idx (because everyone after shifted left by 1).
        # If elim_idx was the last element, it wraps to 0.
        leader_idx = elim_idx % len(children)

    print(*(results))

if __name__ == "__main__":
    solve()