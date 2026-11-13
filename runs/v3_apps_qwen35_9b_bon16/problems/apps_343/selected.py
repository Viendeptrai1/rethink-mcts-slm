import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        p = int(next(iterator))
        x = int(next(iterator))
        y = int(next(iterator))
        
        a = []
        for _ in range(k):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    # We need to add m = n - k marks.
    # Constraints:
    # 1. Sum of all marks <= x
    # 2. Median of all marks >= y
    # Marks must be between 1 and p.
    
    current_sum = sum(a)
    m = n - k
    
    # Strategy:
    # To satisfy the median constraint with minimum cost to the sum, we should try to make the median exactly y (or higher if forced).
    # Since n is odd, the median is the element at index (n+1)//2 - 1 (0-based) in the sorted array.
    # Let's try to construct a valid array.
    # We want to minimize the sum to stay under x.
    # The best way to minimize sum while keeping median >= y is:
    # - Fill as many elements as possible with 1.
    # - Ensure that at least (n // 2 + 1) elements are >= y.
    # To minimize sum, we make exactly (n // 2 + 1) elements equal to y (the smallest valid value for those positions), 
    # and the rest (n // 2) elements equal to 1.
    
    # However, we have existing marks 'a'. We cannot change them.
    # So we need to check if it's possible to form a sequence of length n containing 'a' plus m ones/y's
    # such that:
    # 1. The median is >= y.
    # 2. Total sum <= x.
    
    # Let's calculate the minimum possible sum required to satisfy the median condition.
    # The condition "median >= y" means that in the sorted array of n elements, the element at index (n+1)//2 - 1 must be >= y.
    # This implies that there must be at least (n // 2 + 1) elements in the array that are >= y.
    
    # Let's count how many elements in 'a' are already >= y.
    count_ge_y = sum(1 for val in a if val >= y)
    count_lt_y = sum(1 for val in a if val < y)
    
    # We need total (n // 2 + 1) elements >= y.
    needed_ge_y = n // 2 + 1
    
    # If we already have enough, great. If not, we must fill the remaining needed spots with y (since y is the minimum valid mark for that rank to minimize sum).
    # Actually, we can fill with any value >= y, but to minimize sum, we pick y.
    
    # But wait, we also have existing values < y. These count towards the "lower half".
    # The median is the middle element.
    # Let's sort the hypothetical final array.
    # Let the sorted array be S[0]...S[n-1].
    # We need S[n//2] >= y.
    # This means S[0]...S[n//2] can be anything, but at least one of them (specifically S[n//2]) must be >= y.
    # Actually, if S[n//2] >= y, then S[n//2], S[n//2+1], ... S[n-1] are all >= y.
    # So there must be at least n - (n//2) = n//2 + 1 elements >= y.
    
    # So the requirement is: count of elements >= y must be >= n//2 + 1.
    
    # We have 'count_ge_y' from input.
    # We have m slots to fill.
    # We can choose to fill some slots with y (or more) and some with 1.
    # To minimize sum, we want as many 1s as possible, and only fill the necessary number of slots with y (or larger).
    # However, we cannot change the existing 'a'.
    # If we have too many elements < y in 'a', we might not be able to fix the median without using more than m slots?
    # No, we just need the final count of >= y to be >= needed_ge_y.
    # If count_ge_y >= needed_ge_y, we are good on the count side. We can fill the rest with 1s.
    # If count_ge_y < needed_ge_y, we need to add (needed_ge_y - count_ge_y) elements that are >= y.
    # Since we want to minimize sum, we should add exactly (needed_ge_y - count_ge_y) elements equal to y, 
    # and the remaining m - (needed_ge_y - count_ge_y) elements equal to 1.
    
    # Is it possible that adding y's is not enough?
    # No, because we can always pick y. The only constraint is the sum.
    # Also, we must ensure that we don't accidentally create a situation where the median drops below y?
    # No, the logic "count of >= y >= needed_ge_y" guarantees the median is >= y regardless of distribution, 
    # provided we sort correctly.
    # Wait, is that true?
    # Example: n=5, needed=3. Array: 1, 1, 5, 5, 5. Sorted: 1,1,5,5,5. Median is 5 >= y (if y=5). Count >= 5 is 3. OK.
    # Example: n=5, needed=3. Array: 5, 5, 5, 1, 1. Sorted: 1,1,5,5,5. Median 5.
    # Example: n=5, needed=3. Array: 2, 2, 2, 1, 1. y=2. Count >= 2 is 3. Median 2.
    # Yes, if there are at least n//2 + 1 elements >= y, then when sorted, the element at index n//2 (which is the (n//2+1)-th element) will be one of those >= y elements.
    # Because there are at least n//2 + 1 such elements, they must occupy positions from index (n - (n//2 + 1)) to n-1 in the sorted array?
    # Let k be the count of elements >= y. k >= n//2 + 1.
    # In sorted array, the largest k elements are >= y.
    # Their indices are n-k, n-k+1, ..., n-1.
    # The smallest index among them is n-k.
    # We need the median index (n//2) to be >= y.
    # So we need n-k <= n//2.
    # k >= n - n//2 = n - (n-1)/2 = (n+1)/2 = n//2 + 1 (since n is odd).
    # So yes, the condition is exactly: count(>= y) >= n//2 + 1.
    
    # So the plan:
    # 1. Calculate how many additional >= y we need.
    #    needed_add = max(0, (n // 2 + 1) - count_ge_y)
    # 2. The number of 1s we can add is m - needed_add.
    #    If m < needed_add, then it's impossible (we don't have enough slots to reach the required count of >= y).
    #    In that case, output -1.
    # 3. Construct the new marks:
    #    - 'needed_add' marks of value y.
    #    - 'm - needed_add' marks of value 1.
    # 4. Calculate total sum = current_sum + needed_add * y + (m - needed_add) * 1.
    # 5. If total_sum > x, then output -1.
    # 6. Otherwise, output the constructed marks.
    
    # Wait, is it always optimal to use 1 for the lower ones?
    # Yes, because 1 is the minimum possible mark. Using anything higher increases the sum without helping the median (since they are < y and won't count towards the >= y count).
    # And for the >= y part, y is the minimum possible mark that satisfies the condition. Using anything higher increases sum.
    
    # Edge case: What if we have existing marks >= y, but we add 1s, and somehow the median drops?
    # As proven above, as long as the final count of >= y is >= n//2 + 1, the median is >= y.
    # The values of the other elements don't matter for the median condition, only the count.
    
    needed_add = max(0, (n // 2 + 1) - count_ge_y)
    
    if needed_add > m:
        print("-1")
        return
    
    num_ones = m - needed_add
    
    new_marks = []
    new_marks.extend([y] * needed_add)
    new_marks.extend([1] * num_ones)
    
    # We can output them in any order. The problem asks for "n-k space-separated integers".
    # Let's just output them.
    
    final_sum = current_sum + needed_add * y + num_ones * 1
    
    if final_sum > x:
        print("-1")
        return
    
    # Output the marks
    print(*(new_marks))

if __name__ == "__main__":
    solve()