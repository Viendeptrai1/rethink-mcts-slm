def min_dollars_to_win_tournament(n, a):
    # Find the index of your friend
    friend_index = a.index(-1)
    a[friend_index] = 0  # Treat your friend's bribe cost as zero for convenience

    total_cost = 0

    # Iterate over each stage of the tournament
    for stage in range(int(n.bit_length()) - 1):
        # Calculate the number of boxers advancing to the next stage
        advancing_boxers = n >> (stage + 1)

        # Create a list of pairs and their costs
        pairs = []
        for i in range(0, n, 2):
            pairs.append((a[i], a[i + 1]))

        # Sort pairs by the maximum bribe cost in each pair
        pairs.sort(key=lambda x: max(x[0], x[1]))

        # Select the best pairs to advance
        for i in range(advancing_boxers):
            total_cost += pairs[i][0] if pairs[i][0] < pairs[i][1] else pairs[i][1]

        # Update the list of boxers for the next stage
        a = [pairs[i][0] if pairs[i][0] < pairs[i][1] else pairs[i][1] for i in range(advancing_boxers)]
        n = advancing_boxers

    return total_cost

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(min_dollars_to_win_tournament(n, a))