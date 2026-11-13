import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = []
    for i in range(1, 2 * n + 1):
        a.append(int(input_data[i]))
    
    total_sum = sum(a)
    
    # If total sum is odd, it's impossible to split into two equal integer sums.
    # However, the problem asks if we can make the two sums NOT equal.
    # If total_sum is odd, they can never be equal, so any permutation works.
    # If total_sum is even, we need to check if it's possible to have unequal halves.
    # The only case where we CANNOT have unequal halves is if ALL permutations result in equal halves.
    # This happens if and only if all elements are equal.
    # Why? If all elements are equal (say x), then any split of n elements vs n elements gives sum = n*x vs n*x.
    # If there is at least one element different from the others, we can usually rearrange to break equality.
    # Actually, a simpler logic:
    # If all elements are the same, output -1.
    # Otherwise, we can always construct a valid permutation.
    
    # Check if all elements are equal
    first_elem = a[0]
    all_equal = True
    for x in a:
        if x != first_elem:
            all_equal = False
            break
    
    if all_equal:
        print("-1")
        return
    
    # If not all equal, we need to construct a permutation where sum(first n) != sum(last n).
    # Strategy: Sort the array.
    # Let sorted array be s[0]...s[2n-1].
    # Consider the sum of the first n elements in sorted order vs last n.
    # If they are not equal, we are done.
    # If they are equal, we try swapping one element from the first half with one from the second half.
    # Since not all elements are equal, there exists some s[i] != s[j].
    # If the initial split (sorted) has equal sums, it implies sum(s[0]..s[n-1]) == sum(s[n]..s[2n-1]).
    # Since the total sum is even (otherwise they couldn't be equal), let total = 2S.
    # If we swap s[i] (from first half) and s[j] (from second half), the new sums become:
    # S1' = S1 - s[i] + s[j]
    # S2' = S2 - s[j] + s[i]
    # We want S1' != S2'. Since S1 = S2 initially, this is equivalent to S1 - s[i] + s[j] != S1 - s[j] + s[i]
    # => -s[i] + s[j] != -s[j] + s[i]
    # => 2*s[j] != 2*s[i]
    # => s[j] != s[i]
    # So as long as we can find i < n and j >= n such that s[i] != s[j], swapping them will work.
    # Since not all elements are equal, and the array is sorted, if s[0] != s[n-1], then certainly s[0] != s[n] (if n>=1).
    # Even if s[0] == ... == s[n-1] but s[n] is different, then s[n-1] != s[n].
    # So there must be a difference between the set of first n and last n in a sorted array if not all elements are equal.
    
    a.sort()
    
    sum_first = sum(a[:n])
    sum_last = sum(a[n:])
    
    if sum_first != sum_last:
        print(*(a))
    else:
        # Sums are equal, try to swap.
        # Find an index i in [0, n-1] and j in [n, 2n-1] such that a[i] != a[j].
        # Since not all elements are equal, such a pair must exist.
        # In a sorted array, if a[n-1] == a[n], then the middle is uniform.
        # If a[0] != a[n-1], then a[0] != a[n] (since a[n] >= a[n-1]).
        # If a[0] == a[n-1], then all first half are equal. If a[n-1] != a[n], then a[n-1] != a[n].
        # So checking a[n-1] and a[n] is sufficient? 
        # Wait, if a[n-1] == a[n], then all elements from 0 to 2n-1 might be equal? No, we checked all_equal.
        # If a[n-1] == a[n], it means the boundary is uniform. But since not all are equal, 
        # there must be a difference somewhere.
        # If a[n-1] == a[n], then a[0]...a[n-1] are all equal to X, and a[n]...a[2n-1] are all equal to Y?
        # Not necessarily, but in sorted array, if a[n-1] == a[n], then the transition happens later or earlier?
        # Actually, if a[n-1] == a[n], then the value at n-1 is same as n.
        # If the whole array is not constant, there must be some index k where a[k] != a[k+1].
        # If k < n, then a[k] (in first half) != a[k+1] (could be in first or second).
        # If k >= n, then a[k] (in second half) != a[k+1] (in second half).
        # We need one from first half and one from second half to be different.
        # If a[n-1] != a[n], we can swap a[n-1] and a[n].
        # If a[n-1] == a[n], then all elements from 0 to 2n-1 are equal? 
        # Proof: If a[n-1] == a[n], and array is sorted.
        # Suppose there is a difference. Let min_val = a[0], max_val = a[2n-1].
        # If min_val == max_val, all equal.
        # If min_val < max_val, then there exists some index k where a[k] < a[k+1].
        # If k < n-1, then a[k] is in first half. a[k+1] is in first half (if k+1 < n) or second (if k+1=n).
        # This logic is getting complicated. Simpler:
        # Just iterate to find any i < n and j >= n with a[i] != a[j].
        # Since not all elements are equal, and we have 2n elements, such a pair MUST exist.
        # Why? If for all i < n and j >= n, a[i] == a[j], then all elements in first half equal all elements in second half.
        # Thus all 2n elements are equal. Contradiction.
        
        i = -1
        j = -2
        for idx in range(n):
            if a[idx] != a[n]: # Compare with first element of second half
                i = idx
                j = n
                break
            # If a[idx] == a[n], then a[idx] == a[n] == a[n+1] ... == a[2n-1] (since sorted)
            # So if we don't find a difference with a[n], then all first half are equal to all second half.
            # But we know not all are equal. So the loop will find something or we need to check differently.
            # Actually, if a[0]...a[n-1] are all X, and a[n]...a[2n-1] are all Y.
            # If X == Y, then all equal.
            # If X != Y, then a[0] != a[n].
            # So checking a[0] vs a[n] is sufficient?
            # Yes, because if a[0] == a[n], then since sorted, a[0] <= ... <= a[n-1] <= a[n] <= ...
            # So a[0] = a[n] implies a[0] = a[1] = ... = a[n] = ... = a[2n-1].
            # So if not all equal, a[0] != a[n].
            # Therefore, swapping a[0] and a[n] is always sufficient if sums are equal and not all equal.
        
        # Swap a[0] and a[n]
        a[0], a[n] = a[n], a[0]
        print(*(a))

if __name__ == '__main__':
    solve()