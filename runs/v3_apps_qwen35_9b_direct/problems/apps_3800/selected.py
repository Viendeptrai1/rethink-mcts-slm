import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    a = int(input_data[0])
    s = input_data[1]
    n = len(s)
    
    # Convert string to list of integers
    digits = [int(c) for c in s]
    
    # If a is 0, we need to count rectangles where sum of products is 0.
    # Since b_ij = s_i * s_j, the sum over a rectangle is (sum s_i for i in x..y) * (sum s_j for j in z..t).
    # The product is 0 if either sum is 0.
    # However, the general formula works for a=0 as well if we handle the logic correctly.
    # But let's stick to the general approach first.
    
    # Precompute prefix sums of digits to quickly calculate sum of subsegments
    # prefix_sum[i] = sum(digits[0]...digits[i-1])
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i+1] = prefix_sum[i] + digits[i]
    
    # Function to get sum of digits from index l to r (inclusive, 0-based)
    def get_digit_sum(l, r):
        return prefix_sum[r+1] - prefix_sum[l]
    
    # We need to find number of pairs of subsegments (i1, i2) and (j1, j2) such that:
    # (sum(digits[i1..i2]) * sum(digits[j1..j2])) == a
    
    # Let S1 be the sum of digits in the row range, S2 be the sum of digits in the column range.
    # We need S1 * S2 = a.
    
    # Step 1: Find all possible values of S1 and how many times they occur.
    # Since |s| <= 4000, O(n^2) to find all subsegment sums is acceptable (16 million ops).
    
    from collections import defaultdict
    count_s1 = defaultdict(int)
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += digits[j]
            count_s1[current_sum] += 1
            
    # Step 2: Iterate through all possible values of S1 that are factors of a (or just iterate all keys)
    # If a == 0:
    #   We need S1 * S2 = 0. This happens if S1 == 0 OR S2 == 0.
    #   Using inclusion-exclusion: Count(S1=0) * Total_S2 + Total_S1 * Count(S2=0) - Count(S1=0)*Count(S2=0)
    #   But wait, the formula is simply: sum over all valid (S1, S2) pairs of (count_s1[S1] * count_s2[S2]).
    #   If a=0, valid pairs are (0, any) and (any, 0).
    #   Actually, simpler: iterate all S1 in count_s1. If S1 == 0, then S2 can be anything.
    #   If S1 != 0, then S2 must be a/a.
    
    # Let's generalize:
    # If a == 0:
    #   ans = count_s1[0] * total_subsegments + total_subsegments * count_s2[0] - count_s1[0] * count_s2[0]
    #   Wait, no. The condition is S1 * S2 = 0.
    #   This is the union of (S1=0) and (S2=0).
    #   Size = |S1=0| * Total_S2 + Total_S1 * |S2=0| - |S1=0| * |S2=0|
    #   Where Total_S1 = total number of subsegments = n*(n+1)/2.
    #   But note: count_s1 stores the frequency of each sum. The sum of all frequencies is Total_S1.
    #   So if a=0:
    #     ans = count_s1[0] * (n*(n+1)//2) + (n*(n+1)//2) * count_s2[0] - count_s1[0] * count_s2[0]
    #   Since the distribution of sums is the same for rows and columns (same string s), count_s1 == count_s2.
    #   Let T = n*(n+1)//2. Let Z = count_s1[0].
    #   ans = Z * T + T * Z - Z * Z = 2*T*Z - Z*Z = Z * (2*T - Z).
    
    # If a != 0:
    #   We need S1 * S2 = a.
    #   Iterate over all S1 in count_s1. If S1 divides a, then S2 = a // S1.
    #   If S2 exists in count_s1, add count_s1[S1] * count_s1[S2].
    
    total_subsegments = n * (n + 1) // 2
    
    if a == 0:
        z = count_s1[0]
        ans = z * (2 * total_subsegments - z)
        print(ans)
    else:
        ans = 0
        # Iterate over unique sums present
        for s1, cnt1 in count_s1.items():
            if a % s1 == 0:
                s2 = a // s1
                if s2 in count_s1:
                    ans += cnt1 * count_s1[s2]
        print(ans)

if __name__ == '__main__':
    solve()