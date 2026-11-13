import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    probs = []
    idx = 1
    for _ in range(n):
        probs.append(float(input_data[idx]))
        idx += 1

    probs.sort(reverse=True)

    best_prob = 0.0

    # Case 1: Ask 0 friends -> probability of exactly 1 problem is 0.
    # We can skip this as best_prob is initialized to 0.0.

    # Try all possible sizes from 1 to n
    for k in range(1, n + 1):
        # Calculate probability of exactly 1 success with the top k friends
        # P(exactly 1) = P(friend 1 succeeds) * P(others fail) + ...
        # = sum over i in 0..k-1 of (p[i] * product of (1-p[j]) for j != i in 0..k-1)
        
        # Optimization: 
        # Let S = product of (1-p[j]) for j in 0..k-1
        # Then P(exactly 1) = sum(p[i]) * S? No, because p[i] is not multiplied by the full S.
        # Actually: term_i = p[i] * (S / (1-p[i]))
        # So P = S * sum(p[i] / (1-p[i]))
        
        # However, if any p[i] is 1.0, then (1-p[i]) is 0, division by zero.
        # If we have a 1.0, and we pick k friends including it:
        # If we pick exactly one 1.0 and others are < 1.0, prob = 1 * product(others fail)
        # If we pick more than one friend where at least one is 1.0, prob = 0 (more than 1 problem guaranteed)
        # If we pick multiple 1.0s, prob = 0.
        
        # Let's compute directly to avoid division issues and keep it simple given n <= 100.
        
        current_prob = 0.0
        # Precompute product of (1-p) for all selected
        # But since k is small, we can just loop.
        
        # Select top k
        selected_probs = probs[:k]
        
        # Calculate P(exactly 1)
        # Iterate each friend, assume they succeed, others fail
        for i in range(k):
            p_i = selected_probs[i]
            # Probability others fail
            others_fail = 1.0
            for j in range(k):
                if i != j:
                    others_fail *= (1.0 - selected_probs[j])
            
            current_prob += p_i * others_fail
        
        if current_prob > best_prob:
            best_prob = current_prob

    print(f"{best_prob:.12f}")

if __name__ == "__main__":
    solve()