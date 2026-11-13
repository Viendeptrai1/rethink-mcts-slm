import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    results = []
    
    for _ in range(t):
        a = int(next(iterator))
        b = int(next(iterator))
        
        if a == b:
            results.append(0)
            continue
        
        diff = abs(a - b)
        
        # Find the smallest k such that sum(1..k) >= diff
        # k*(k+1)/2 >= diff
        # k^2 + k - 2*diff >= 0
        # Using quadratic formula: k = (-1 + sqrt(1 + 8*diff)) / 2
        import math
        k = int((-1 + math.isqrt(1 + 8 * diff)) // 2)
        
        # Check if k is sufficient
        current_sum = k * (k + 1) // 2
        if current_sum < diff:
            k += 1
            current_sum = k * (k + 1) // 2
        
        # Now current_sum >= diff. We need to check the parity.
        # The sum of 1..k has a certain parity.
        # We need to distribute the extra (current_sum - diff) among the operations.
        # Adding 1 to a number changes its parity.
        # If we add 1 to one of the operations (i.e., increase the value added by 1),
        # the total sum increases by 1, and the parity of the total sum flips.
        # However, we can only increase the values added if we have "spare" sum.
        # Actually, the logic is:
        # We have added 1+2+...+k = S.
        # We need to reach exactly diff.
        # If S == diff, we are good.
        # If S > diff, let rem = S - diff.
        # We need to reduce the total added amount by rem.
        # But we can't reduce. We can only choose to add to a or b differently.
        # Wait, the problem says: "increase it by 1", "increase it by 2", etc.
        # We assign each step i (value i) to either a or b.
        # Let S_a be sum of steps assigned to a, S_b be sum of steps assigned to b.
        # We want a + S_a = b + S_b => S_a - S_b = b - a = diff (assuming b > a).
        # Also S_a + S_b = S_total = k*(k+1)/2.
        # Adding equations: 2*S_a = S_total + diff.
        # So S_total + diff must be even.
        # If (S_total + diff) is odd, we need to increase S_total by 1 (make it even relative to diff).
        # Increasing k by 1 adds k+1 to the sum.
        # So we check parity of (S_total + diff).
        # If (S_total + diff) % 2 != 0, we need one more operation.
        # If we do k+1, new sum S' = S + (k+1).
        # New parity check: (S' + diff) % 2.
        # Since S' = S + k + 1, the change in parity depends on (k+1).
        # If (S + diff) is odd, we need to add an odd number to S to make (S+diff) even?
        # No, we need (S_new + diff) to be even.
        # Currently (S + diff) is odd.
        # If we add 1 operation (value k+1), S_new = S + k + 1.
        # (S_new + diff) = S + diff + k + 1.
        # We need this to be even.
        # Since S+diff is odd, we need k+1 to be odd.
        # If k+1 is odd, then adding 1 operation fixes the parity.
        # If k+1 is even, then adding 1 operation keeps it odd, so we need to add 2 operations.
        
        if (current_sum + diff) % 2 == 0:
            results.append(k)
        else:
            # Try k+1
            k += 1
            current_sum = k * (k + 1) // 2
            if (current_sum + diff) % 2 == 0:
                results.append(k)
            else:
                # Try k+2
                k += 1
                results.append(k)
    
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()