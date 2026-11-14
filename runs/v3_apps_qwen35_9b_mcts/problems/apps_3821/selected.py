import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    p = []
    for i in range(n):
        p.append(float(input_data[i + 1]))

    # Sort probabilities in descending order
    p.sort(reverse=True)

    max_prob = 0.0

    # Try all possible prefixes of the sorted list
    # The optimal set is always a prefix of the sorted probabilities
    current_zero = 1.0  # Probability of 0 successes with empty set
    current_one = 0.0   # Probability of 1 success with empty set

    for i in range(n):
        prob = p[i]
        # When adding a new friend with probability 'prob':
        # New zero successes = old_zero * (1 - prob)
        # New one success = old_zero * prob + old_one * (1 - prob)
        new_zero = current_zero * (1.0 - prob)
        new_one = current_zero * prob + current_one * (1.0 - prob)

        current_zero = new_zero
        current_one = new_one

        if current_one > max_prob:
            max_prob = current_one

    print(f"{max_prob:.12f}")

if __name__ == "__main__":
    solve()