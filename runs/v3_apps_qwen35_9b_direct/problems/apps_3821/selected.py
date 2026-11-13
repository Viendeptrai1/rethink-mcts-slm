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

    best_prob = 0.0

    # Try all possible subsets by taking the top k friends with the highest probabilities
    # It is optimal to consider only prefixes of the sorted array.
    current_prob_one = 0.0
    current_prob_none = 1.0

    # Case: choose 0 friends -> probability of exactly 1 problem is 0.0
    # We start checking from k=1 to n

    for k in range(1, n + 1):
        # We are considering the set of the first k friends (after sorting)
        # Calculate probability of exactly one success among these k friends
        
        # We can compute this iteratively or directly.
        # Let's compute directly for clarity: sum over i in 0..k-1 of (p[i] * product of (1-p[j]) for j != i)
        # However, an iterative update is more efficient.
        
        # Let's re-calculate from scratch for each k to avoid state confusion, 
        # since n is small (<= 100). O(n^2) is perfectly fine.
        
        prob = 0.0
        for i in range(k):
            # Probability that friend i succeeds and all others in the set fail
            term = p[i]
            for j in range(k):
                if i == j:
                    continue
                term *= (1.0 - p[j])
            prob += term
        
        if prob > best_prob:
            best_prob = prob

    print(f"{best_prob:.12f}")

if __name__ == "__main__":
    solve()