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

    # Sort the powers in ascending order
    a.sort()

    # We will try removing i elements from the end (smallest elements)
    # Actually, to maximize average, we should remove the smallest elements.
    # So if we remove i elements, we remove the first i elements of the sorted array.
    # The remaining elements are a[i:]
    
    # We can iterate on the number of removals 'i' from 0 to n-1.
    # We cannot remove all n elements because the problem says "if there are at least two" to remove.
    # Wait, the problem says: "remove one superhero from their team (if there are at least two)".
    # This implies we must have at least 2 superheroes to perform a removal.
    # However, once we have 1 superhero, can we remove them? No, because condition "at least two" fails.
    # So the minimum number of superheroes remaining is 1? 
    # Let's re-read carefully: "remove one superhero from their team (if there are at least two)".
    # This means if current size is S, we can remove if S >= 2. Resulting size S-1.
    # If size becomes 1, we cannot remove anymore.
    # So the final team size can be anywhere from 1 to n.
    # But wait, if we start with n=1, we can't remove.
    # If we start with n=2, we can remove one, leaving 1. Then we can't remove anymore.
    # So yes, final size >= 1.
    
    # Strategy:
    # Iterate over the number of elements to remove, say 'rem'.
    # rem can range from 0 to n-1.
    # If we remove 'rem' elements, we remove the 'rem' smallest elements (since sorted).
    # The remaining elements are a[rem], a[rem+1], ..., a[n-1].
    # Let count = n - rem.
    # We have 'm' total operations.
    # We can use some operations to increase the powers of the remaining 'count' superheroes.
    # Constraint: each superhero can be increased at most 'k' times.
    # Total capacity to increase = count * k.
    # We can use at most 'm' operations.
    # So actual increase we can apply = min(m, count * k).
    # To maximize the average, we should distribute this increase as evenly as possible among the remaining superheroes.
    # Why? Because average = (sum + total_increase) / count.
    # The sum of the remaining elements is fixed for a given 'rem'.
    # The total increase is fixed (min(m, count*k)) regardless of distribution, as long as we don't exceed k per person.
    # Since we can distribute up to k per person, and we have total capacity count*k, 
    # if m <= count*k, we can just add m to the sum.
    # If m > count*k, we can only add count*k to the sum.
    # So the formula for max average for a fixed 'rem' is:
    #   base_sum = sum(a[rem:])
    #   add = min(m, (n - rem) * k)
    #   avg = (base_sum + add) / (n - rem)
    
    # We need to find the maximum of this value over all valid 'rem'.
    # Valid 'rem': 0 to n-1.
    
    # Optimization:
    # Calculating sum(a[rem:]) repeatedly is O(n^2). We need O(n).
    # We can precompute suffix sums.
    
    suffix_sum = [0] * (n + 1)
    current_sum = 0
    for i in range(n - 1, -1, -1):
        current_sum += a[i]
        suffix_sum[i] = current_sum
    
    max_avg = 0.0
    
    # Try removing i elements, where i goes from 0 to n-1
    for i in range(n):
        count = n - i
        # Sum of remaining elements
        current_sum_val = suffix_sum[i]
        
        # Max increase possible
        total_capacity = count * k
        add = m if m < total_capacity else total_capacity
        
        avg = (current_sum_val + add) / count
        
        if avg > max_avg:
            max_avg = avg
            
    print(f"{max_avg:.20f}")

if __name__ == '__main__':
    solve()