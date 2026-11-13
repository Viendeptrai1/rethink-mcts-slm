def count_integers(N, X, A):
    MOD = 998244353

    # Convert binary strings to integers
    X = int(X, 2)
    A = [int(a, 2) for a in A]

    # Use a set to track all possible numbers on the board
    possible_numbers = set(A)

    # Use a queue to perform BFS
    from collections import deque
    queue = deque(A)

    while queue:
        current = queue.popleft()

        # Double the current number
        doubled = current * 2
        if doubled <= X and doubled not in possible_numbers:
            possible_numbers.add(doubled)
            queue.append(doubled)

        # XOR with all other numbers, including itself
        for num in A:
            xored = current ^ num
            if xored <= X and xored not in possible_numbers:
                possible_numbers.add(xored)
                queue.append(xored)

    # Return the count of unique numbers modulo MOD
    return len(possible_numbers) % MOD

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
X = data[1]
A = data[2:]

# Output the result
print(count_integers(N, X, A))