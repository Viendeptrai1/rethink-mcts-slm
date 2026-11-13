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
    # Precompute the remainders modulo 3 for the sequence a[i] = i*i - i + 1
    # Note: i starts from 1 to n
    # Let's analyze the pattern of (i*i - i + 1) % 3
    # i=1: 1-1+1 = 1 -> 1 % 3 = 1
    # i=2: 4-2+1 = 3 -> 3 % 3 = 0
    # i=3: 9-3+1 = 7 -> 7 % 3 = 1
    # i=4: 16-4+1 = 13 -> 13 % 3 = 1
    # i=5: 25-5+1 = 21 -> 21 % 3 = 0
    # i=6: 36-6+1 = 31 -> 31 % 3 = 1
    # i=7: 49-7+1 = 43 -> 43 % 3 = 1
    # i=8: 64-8+1 = 57 -> 57 % 3 = 0
    # Pattern of remainders for i=1,2,3,...: 1, 0, 1, 1, 0, 1, 1, 0, ...
    # It repeats every 3: [1, 0, 1]
    
    # Count how many numbers in the sequence have remainder 0, 1, or 2 modulo 3
    count0 = 0  # remainder 0
    count1 = 0  # remainder 1
    count2 = 0  # remainder 2
    
    for i in range(1, n + 1):
        val = i * i - i + 1
        rem = val % 3
        if rem == 0:
            count0 += 1
        elif rem == 1:
            count1 += 1
        else:
            count2 += 1
    
    # We need to find triples (a[i], a[j], a[k]) with i < j < k such that
    # (a[i] + a[j] + a[k]) % 3 == 0
    # This happens if the sum of their remainders is divisible by 3.
    # Possible combinations of remainders (r1, r2, r3) that sum to 0 mod 3:
    # (0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 1, 2)
    
    # Number of ways to choose 3 from count0: C(count0, 3)
    # Number of ways to choose 3 from count1: C(count1, 3)
    # Number of ways to choose 3 from count2: C(count2, 3)
    # Number of ways to choose one from each: count0 * count1 * count2
    
    def combinations(n, k):
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1
        if k > n // 2:
            k = n - k
        res = 1
        for i in range(k):
            res = res * (n - i) // (i + 1)
        return res
    
    result = (combinations(count0, 3) + 
              combinations(count1, 3) + 
              combinations(count2, 3) + 
              count0 * count1 * count2)
    
    return result