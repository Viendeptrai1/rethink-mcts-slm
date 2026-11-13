import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))
    m = int(next(iterator))
    
    a = []
    for _ in range(n):
        a.append(int(next(iterator)))
    
    # Sort powers to easily access smallest
    a.sort()
    
    # Strategy:
    # We can remove elements from the smallest end to increase the average.
    # For a fixed number of removed elements 'i', we have (n-i) elements left.
    # The sum of these remaining elements is fixed (initial sum - sum of removed).
    # We have 'm' total operations. Each removal counts as 1 op.
    # So, if we remove 'i' elements, we have (m - i) operations left to increase powers.
    # We should distribute these (m - i) increases on the largest (n-i) elements.
    # Constraint: Each element can be increased at most 'k' times.
    # So for each of the (n-i) elements, we can add at most k.
    # Max total increase = (n - i) * k.
    # Actual increase we can apply = min(m - i, (n - i) * k).
    
    # We iterate on the number of elements to remove, from 0 to n-1 (must keep at least 1).
    # Since n is up to 10^5, we need an efficient way.
    # As we increase i (remove more small elements), the base sum increases (relative to average) 
    # but the number of elements decreases.
    # The function f(i) = (sum of largest n-i) + min(m-i, (n-i)*k) is what we maximize divided by (n-i).
    
    # Let's compute prefix sums to quickly get sum of smallest i elements.
    prefix_sum = [0] * (n + 1)
    for idx in range(n):
        prefix_sum[idx + 1] = prefix_sum[idx] + a[idx]
    
    total_sum = prefix_sum[n]
    
    best_avg = 0.0
    
    # Iterate i from 0 to n-1
    # i is the number of elements removed (always the smallest ones)
    for i in range(n):
        count = n - i
        
        # Sum of the remaining elements (largest 'count' elements)
        current_sum = total_sum - prefix_sum[i]
        
        # Operations spent on removal
        ops_spent = i
        
        if ops_spent > m:
            break
        
        ops_left = m - ops_spent
        
        # Maximum possible increase given per-element limit k
        max_possible_increase = count * k
        
        # Actual increase we can apply
        actual_increase = min(ops_left, max_possible_increase)
        
        final_sum = current_sum + actual_increase
        avg = final_sum / count
        
        if avg > best_avg:
            best_avg = avg
            
    print(f"{best_avg:.20f}")

if __name__ == "__main__":
    solve()