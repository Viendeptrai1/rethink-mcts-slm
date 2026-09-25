import sys
from collections import defaultdict
import heapq

def main():
    import sys
    import heapq
    from collections import defaultdict

    def read_ints():
        return list(map(int, sys.stdin.readline().split()))

    n, m = read_ints()
    a = read_ints()
    segments = [read_ints() for _ in range(m)]

    # Create a dictionary to store the segments that affect each position
    pos_to_segments = defaultdict(list)
    for j, (l, r) in enumerate(segments):
        pos_to_segments[l].append((j, -1))
        pos_to_segments[r + 1].append((j, 1))

    # Initialize the current state of the array
    current_state = [0] * (n + 1)
    max_value = min_value = 0
    max_diff = 0
    best_segments = []

    # Priority queue to keep track of the segments that are currently active
    active_segments = []
    for i in range(1, n + 1):
        # Apply the changes from the segments that start or end at position i
        for j, delta in pos_to_segments[i]:
            if delta == -1:
                heapq.heappush(active_segments, (-segments[j][1], j))
            else:
                while active_segments and active_segments[0][1] == j:
                    heapq.heappop(active_segments)

        # Update the current state of the array
        current_state[i] = current_state[i - 1] + len(active_segments)

        # Update the maximum and minimum values
        max_value = max(max_value, current_state[i])
        min_value = min(min_value, current_state[i])

        # Update the maximum difference
        if max_value - min_value > max_diff:
            max_diff = max_value - min_value
            best_segments = [j for _, j in active_segments]

    # Print the result
    print(max_diff)
    print(len(best_segments))
    print(*best_segments)

if __name__ == "__main__":
    main()