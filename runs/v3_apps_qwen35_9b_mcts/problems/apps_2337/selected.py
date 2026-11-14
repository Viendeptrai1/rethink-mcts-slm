import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    a = []
    for i in range(n):
        a.append(int(data[2 + i]))
    
    b = []
    for i in range(m):
        b.append(int(data[2 + n + i]))
    
    # Sort both arrays to allow greedy matching
    a.sort()
    b.sort()
    
    # Greedy strategy:
    # Try to satisfy the smallest requirement 'a[i]' with the smallest available problem 'b[j]'
    # that is >= a[i]. If we find one, we use it (increment j). If not, we can't satisfy this requirement
    # with existing problems, so we would need to create a new one.
    # However, since we want to maximize the number of satisfied requirements (to minimize new ones),
    # we iterate through requirements and try to match them with the best available problem.
    
    # Actually, a simpler greedy approach for this specific structure:
    # Iterate through the sorted requirements. For each requirement, try to find the smallest available
    # problem that satisfies it. If we find one, we use it. If not, we count it as needing a new problem.
    # But wait, simply iterating and picking the first valid might not be optimal if we skip a problem
    # that could have been used for a later requirement? 
    # No, because if b[j] >= a[i], and we have a later requirement a[k] > a[i], then b[j] might also be >= a[k]
    # or not. Using the smallest valid b[j] for a[i] is optimal because it saves larger b's for larger a's.
    
    # Let's refine:
    # We have sorted a and sorted b.
    # Pointer for a: i
    # Pointer for b: j
    # Count of satisfied requirements: satisfied_count
    
    i = 0
    j = 0
    satisfied_count = 0
    
    while i < n and j < m:
        if b[j] >= a[i]:
            # We can satisfy requirement a[i] with problem b[j]
            satisfied_count += 1
            i += 1
            j += 1
        else:
            # b[j] is too small for a[i]. Since b is sorted, b[j] is too small for any a[k] where k >= i.
            # So this problem b[j] is useless for the remaining requirements.
            j += 1
            
    # The number of new problems needed is total requirements - satisfied count
    print(n - satisfied_count)

if __name__ == '__main__':
    solve()