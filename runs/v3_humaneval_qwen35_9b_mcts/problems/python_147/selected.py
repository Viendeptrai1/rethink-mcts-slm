def get_max_triples(n):
    """
    You are given a positive integer n. You have to create an integer array a of length n.
        For each i (1 ≤ i ≤ n), the value of a[i] = i * i - i + 1.
        Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, 
    and a[i] + a[j] + a[k] is a multiple of 3.

    Example :
        Input: n = 5
        Output: 1
        Explanation: 
        a = [1, 3, 7, 13, 21]
        The only valid triple is (1, 7, 13).
    """
    # Calculate remainders modulo 3 for the sequence a[i] = i*i - i + 1
    # Let's analyze the pattern for i starting from 1:
    # i=1: 1*1 - 1 + 1 = 1 -> 1 % 3 = 1
    # i=2: 2*2 - 2 + 1 = 3 -> 3 % 3 = 0
    # i=3: 3*3 - 3 + 1 = 7 -> 7 % 3 = 1
    # i=4: 4*4 - 4 + 1 = 13 -> 13 % 3 = 1
    # i=5: 5*5 - 5 + 1 = 21 -> 21 % 3 = 0
    # i=6: 6*6 - 6 + 1 = 37 -> 37 % 3 = 1
    # i=7: 7*7 - 7 + 1 = 47 -> 47 % 3 = 2
    # i=8: 8*8 - 8 + 1 = 57 -> 57 % 3 = 0
    # i=9: 9*9 - 9 + 1 = 73 -> 73 % 3 = 1
    # i=10: 10*10 - 10 + 1 = 91 -> 91 % 3 = 1
    # i=11: 11*11 - 11 + 1 = 111 -> 111 % 3 = 0
    # i=12: 12*12 - 12 + 1 = 133 -> 133 % 3 = 1
    # i=13: 13*13 - 13 + 1 = 157 -> 157 % 3 = 1
    # i=14: 14*14 - 14 + 1 = 181 -> 181 % 3 = 1
    # i=15: 15*15 - 15 + 1 = 209 -> 209 % 3 = 2
    # i=16: 16*16 - 16 + 1 = 241 -> 241 % 3 = 0
    # i=17: 17*17 - 17 + 1 = 271 -> 271 % 3 = 1
    # i=18: 18*18 - 18 + 1 = 307 -> 307 % 3 = 1
    # i=19: 19*19 - 19 + 1 = 343 -> 343 % 3 = 1
    # i=20: 20*20 - 20 + 1 = 381 -> 381 % 3 = 0
    # i=21: 21*21 - 21 + 1 = 421 -> 421 % 3 = 2
    
    # The pattern of remainders modulo 3 repeats every 6 terms:
    # [1, 0, 1, 1, 0, 2]
    # Let's verify:
    # i=1: 1
    # i=2: 0
    # i=3: 1
    # i=4: 1
    # i=5: 0
    # i=6: 2
    # i=7: 1 (same as i=1)
    # i=8: 0 (same as i=2)
    # ...
    
    # Pattern: [1, 0, 1, 1, 0, 2]
    # Counts in one period of 6:
    # 0: 2 times
    # 1: 3 times
    # 2: 1 time
    
    # We need to count how many full periods and remaining terms
    full_periods = n // 6
    remainder = n % 6
    
    # Count remainders in full periods
    count_0 = full_periods * 2
    count_1 = full_periods * 3
    count_2 = full_periods * 1
    
    # Count remainders in the remaining terms
    # Pattern: [1, 0, 1, 1, 0, 2]
    if remainder > 0:
        if remainder >= 1:
            count_1 += 1
        if remainder >= 2:
            count_0 += 1
        if remainder >= 3:
            count_1 += 1
        if remainder >= 4:
            count_1 += 1
        if remainder >= 5:
            count_0 += 1
        if remainder >= 6:
            count_2 += 1
    
    # Now count valid triples
    # Valid combinations for sum % 3 == 0:
    # 1. Three 0s: C(count_0, 3)
    # 2. Three 1s: C(count_1, 3)
    # 3. Three 2s: C(count_2, 3)
    # 4. One 0, one 1, one 2: count_0 * count_1 * count_2
    
    def combinations(n, k):
        if n < k:
            return 0
        if k == 0:
            return 1
        if k == 1:
            return n
        if k == 2:
            return n * (n - 1) // 2
        if k == 3:
            return n * (n - 1) * (n - 2) // 6
        return 0
    
    result = (combinations(count_0, 3) + 
              combinations(count_1, 3) + 
              combinations(count_2, 3) + 
              count_0 * count_1 * count_2)
    
    return result