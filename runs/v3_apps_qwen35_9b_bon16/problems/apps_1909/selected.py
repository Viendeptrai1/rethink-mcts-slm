import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    a = []
    idx = 2
    for _ in range(n):
        a.append(int(data[idx]))
        idx += 1
    
    # Since n is divisible by k, the number of full cycles is n // k
    # The pattern of tasks Inna catches repeats every k tasks.
    # Specifically, if Dima starts at index i (0-based), Inna catches tasks at indices:
    # i, (i + k) % n, (i + 2*k) % n, ...
    # This means the set of tasks Inna catches depends only on i % k.
    # There are k possible starting positions modulo k: 0, 1, ..., k-1.
    # For each remainder r in [0, k-1], we calculate the total power.
    # Then we find the starting position (1-based index) that minimizes this total power.
    # If there's a tie, we choose the smallest starting position (1-based).
    
    # Let's compute the sum for each remainder r from 0 to k-1.
    # The tasks Inna catches for a start position with remainder r are:
    # r, r+k, r+2k, ... up to < n.
    
    sums = [0] * k
    
    for r in range(k):
        current_sum = 0
        current_idx = r
        while current_idx < n:
            current_sum += a[current_idx]
            current_idx += k
        sums[r] = current_sum
    
    # Now we need to map these sums back to the actual starting positions.
    # A starting position with 1-based index S corresponds to 0-based index S-1.
    # The remainder is (S-1) % k.
    # We want to find S in range [1, n] such that sums[(S-1) % k] is minimized.
    # If multiple S give the same minimum sum, pick the smallest S.
    
    min_total = float('inf')
    best_start = -1
    
    # We iterate through possible remainders r from 0 to k-1.
    # For a fixed remainder r, the smallest starting position S such that (S-1) % k == r is S = r + 1.
    # Any other starting position with the same remainder would be larger (r+1+k, r+1+2k, etc.).
    # Since we want the minimum S in case of ties, for each remainder group, we only care about the smallest S, which is r+1.
    # Therefore, we just compare sums[r] with the current minimum and update best_start to r+1.
    
    for r in range(k):
        if sums[r] < min_total:
            min_total = sums[r]
            best_start = r + 1
            
    print(best_start)

if __name__ == '__main__':
    solve()