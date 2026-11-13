import sys

def solve():
    s_bin = sys.stdin.readline().strip()
    if not s_bin:
        return
    
    # The trains depart at times 4^k = 2^(2k) for k >= 0.
    # We need to count how many such times are strictly less than s.
    # s is given in binary.
    # Let n be the length of the binary string s_bin.
    # The value of s is sum(b_i * 2^i) where b_i is the bit at position i (0-indexed from right).
    # Actually, it's easier to think in terms of the position of the most significant bit.
    # If s has n bits, then 2^(n-1) <= s < 2^n.
    # A train departs at time T = 2^(2k).
    # We need 2^(2k) < s.
    # Taking log2: 2k < log2(s).
    # Since s < 2^n, log2(s) < n.
    # So 2k < n => k < n/2.
    # The number of non-negative integers k satisfying k < n/2 is floor((n-1)/2) if we consider strict inequality carefully?
    # Let's re-evaluate with examples.
    
    # Example 1: s = 100000000 (binary) -> length n=9. Value = 256 = 2^8.
    # Trains: 1 (2^0), 4 (2^2), 16 (2^4), 64 (2^6), 256 (2^8).
    # Strictly before 256: 1, 4, 16, 64. Count = 4.
    # Here n=9. k can be 0, 1, 2, 3. (2*0=0, 2*1=2, 2*2=4, 2*3=6). 2*4=8 is not < 8.
    # So k < 4. Number of values = 4.
    # Formula: k < n/2? 9/2 = 4.5. k < 4.5 => k in {0,1,2,3,4}? No, 2*4=8 which is not < 8.
    # Wait, s = 256. Condition: 2^(2k) < 256 => 2k < 8 => k < 4.
    # So k can be 0, 1, 2, 3. Count = 4.
    # Relationship with n=9: k < (n-1)/2 ? (9-1)/2 = 4. k < 4. Correct.
    
    # Example 2: s = 101 (binary) -> length n=3. Value = 5.
    # Trains: 1 (2^0), 4 (2^2). Next is 16.
    # Strictly before 5: 1, 4. Count = 2.
    # Condition: 2^(2k) < 5.
    # k=0: 1 < 5 (Yes)
    # k=1: 4 < 5 (Yes)
    # k=2: 16 < 5 (No)
    # So k in {0, 1}. Count = 2.
    # n=3. (n-1)/2 = 1. k < 1? No, k can be 0 and 1.
    # Let's check the exponent of the highest power of 2 less than s.
    # Actually, let's just look at the length n.
    # If s = 2^m, then n = m+1.
    # Condition 2^(2k) < 2^m => 2k < m => k < m/2.
    # Number of k is floor((m-1)/2) + 1?
    # If m=8 (s=256), k < 4 => k=0,1,2,3 (4 values). floor((8-1)/2)+1 = 3+1=4. Correct.
    # If m=2 (s=4, binary 100, n=3), k < 1 => k=0 (1 value). But example s=5 (101) gave 2.
    # For s=5, m is not an integer. 2^2 <= 5 < 2^3.
    # Condition 2^(2k) < 5.
    # 2k < log2(5) approx 2.32.
    # 2k can be 0, 2. (k=0, 1).
    # So we need 2k < log2(s).
    # Since s is an integer, 2k < log2(s) is equivalent to 2k <= floor(log2(s)) if log2(s) is not integer?
    # No. If s=5, log2(5)=2.32. 2k < 2.32 => 2k <= 2 => k <= 1.
    # If s=4, log2(4)=2. 2k < 2 => 2k <= 1 => k=0.
    # So the condition is 2k < log2(s).
    # This is equivalent to 2k <= floor(log2(s)) if s is not a power of 2?
    # If s = 2^m, then 2k < m.
    # If s = 2^m + 1, then 2k < m + epsilon => 2k <= m.
    # So generally, let m = floor(log2(s)).
    # If s is a power of 2 (s = 2^m), then we need 2k < m.
    # If s is not a power of 2, then s > 2^m, so log2(s) > m, so 2k < log2(s) allows 2k = m (if m is even).
    # Wait, if s = 2^m + 1, then 2^m < s. If m is even, say m=2k, then 2^(2k) = 2^m < s. So k is included.
    # If s = 2^m, then 2^m is not strictly less than s. So k=m/2 is excluded.
    
    # Let's simplify using the binary string length n.
    # n = number of bits.
    # The highest power of 2 less than or equal to s is 2^(n-1).
    # Let m = n-1.
    # Case 1: s is a power of 2. Then s = 2^m.
    #   We need 2^(2k) < 2^m => 2k < m.
    #   Number of k >= 0 is floor((m-1)/2) + 1?
    #   If m=8, 2k < 8 => k < 4 => k=0,1,2,3 (4 values).
    #   Formula: (m-1)//2 + 1 = 7//2 + 1 = 3+1=4. Correct.
    # Case 2: s is not a power of 2. Then 2^m < s < 2^(m+1).
    #   We need 2^(2k) < s.
    #   Since s > 2^m, if 2k = m, then 2^(2k) = 2^m < s. So k = m/2 is included if m is even.
    #   If m is odd, 2k cannot be m. The largest even number <= m is m-1.
    #   So we need 2k <= m if m is even? No.
    #   If m is even, 2k can be m. Since 2^m < s, 2^(2k) < s holds.
    #   If m is odd, 2k can be m-1. Since 2^(m-1) < 2^m < s, it holds.
    #   So effectively, we need 2k <= m.
    #   Number of k >= 0 such that 2k <= m is floor(m/2) + 1.
    #   Let's check s=5 (101), n=3, m=2. Not power of 2.
    #   Need 2k <= 2 => k=0, 1. Count = 2.
    #   Formula: floor(2/2) + 1 = 1+1=2. Correct.
    #   Check s=6 (110), n=3, m=2. Not power of 2.
    #   Trains: 1, 4. 4 < 6. Count 2.
    #   Formula: 2. Correct.
    #   Check s=7 (111), n=3, m=2. Not power of 2.
    #   Trains: 1, 4. Count 2.
    #   Formula: 2. Correct.
    #   Check s=8 (1000), n=4, m=3. Power of 2.
    #   Trains: 1, 4. (1, 4 < 8). 16 > 8. Count 2.
    #   Formula for power of 2: (3-1)//2 + 1 = 1+1=2. Correct.
    #   Check s=9 (1001), n=4, m=3. Not power of 2.
    #   Trains: 1, 4. Count 2.
    #   Formula for not power of 2: floor(3/2) + 1 = 1+1=2. Correct.
    #   Check s=16 (10000), n=5, m=4. Power of 2.
    #   Trains: 1, 4, 16? No, strictly before. 1, 4. Count 2.
    #   Wait, 16 is 4^2. Strictly before 16 means < 16. So 1, 4. Count 2.
    #   Formula power of 2: (4-1)//2 + 1 = 1+1=2. Correct.
    #   Check s=17 (10001), n=5, m=4. Not power of 2.
    #   Trains: 1, 4, 16. Count 3.
    #   Formula not power of 2: floor(4/2) + 1 = 2+1=3. Correct.
    
    # Summary:
    # n = len(s_bin)
    # m = n - 1
    # Check if s is a power of 2.
    # A binary number is a power of 2 if it has exactly one '1' bit.
    # If s_bin.count('1') == 1:
    #    ans = (m - 1) // 2 + 1
    # Else:
    #    ans = m // 2 + 1
    
    # Let's verify edge case s=1 (binary '1').
    # n=1, m=0. count('1')=1. Power of 2.
    # ans = (0-1)//2 + 1 = -1//2 + 1 = -1 + 1 = 0.
    # Trains before 1: none. Correct.
    
    # s=2 (binary '10').
    # n=2, m=1. count('1')=1. Power of 2.
    # ans = (1-1)//2 + 1 = 0 + 1 = 1.
    # Trains before 2: 1. Correct.
    
    # s=3 (binary '11').
    # n=2, m=1. count('1')=2. Not power of 2.
    # ans = 1//2 + 1 = 0 + 1 = 1.
    # Trains before 3: 1. Correct.
    
    # s=4 (binary '100').
    # n=3, m=2. count('1')=1. Power of 2.
    # ans = (2-1)//2 + 1 = 0 + 1 = 1.
    # Trains before 4: 1. Correct.
    
    # s=5 (binary '101').
    # n=3, m=2. count('1')=2. Not power of 2.
    # ans = 2//2 + 1 = 1 + 1 = 2.
    # Trains before 5: 1, 4. Correct.
    
    # Logic seems solid.
    
    n = len(s_bin)
    m = n - 1
    if s_bin.count('1') == 1:
        ans = (m - 1) // 2 + 1
    else:
        ans = m // 2 + 1
    
    print(ans)

if __name__ == '__main__':
    solve()