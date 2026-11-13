import sys

def solve():
    s_binary = sys.stdin.readline().strip()
    if not s_binary:
        return
    
    # The trains depart at times 4^k = (2^2)^k = 2^(2k) for k >= 0.
    # In binary, 2^(2k) is represented as a '1' followed by 2k zeros.
    # We need to count how many such numbers are strictly less than s.
    #
    # Let the length of the binary string s be L.
    # The value of s is sum(b_i * 2^i) where b_i is the i-th bit (0-indexed from right).
    # A train departs at time T = 2^(2k).
    # T < s if:
    # 1. The bit length of T is less than the bit length of s.
    #    Bit length of T = 2k + 1 (since it's 1 followed by 2k zeros).
    #    So if 2k + 1 < L, then T < s.
    #    This gives us k such that 2k < L - 1 => k < (L - 1) / 2.
    #    Number of such k >= 0 is floor((L - 1) / 2) + 1? Let's re-evaluate.
    #    Actually, number of integers k >= 0 such that 2k + 1 < L is:
    #    2k < L - 1  => k <= (L - 2) // 2.
    #    Count = floor((L - 2) / 2) - 0 + 1 = (L - 2) // 2 + 1 if L >= 2, else 0.
    #    Wait, simpler: k goes from 0 up to some max.
    #    Condition: 2k + 1 < L.
    #    Max k = (L - 2) // 2.
    #    Count = (L - 2) // 2 + 1, provided L >= 2. If L=1, count=0.
    #
    # 2. The bit length of T is equal to the bit length of s (i.e., 2k + 1 = L).
    #    This implies L must be odd. If L is even, no train has the same bit length.
    #    If L is odd, then L = 2k + 1, so k = (L - 1) / 2.
    #    We need to check if T = 2^(L-1) < s.
    #    Since s has L bits and the leading bit is always 1 (no leading zeros),
    #    s = 2^(L-1) + remainder, where remainder >= 0.
    #    T = 2^(L-1).
    #    So T < s is equivalent to remainder > 0, which means s is not a power of 2.
    #    Alternatively, s > 2^(L-1) is true if there is any '1' bit at a position < L-1.
    #    In the binary string s (which has length L), the first character is '1'.
    #    If there is any other '1' in the string, then s > 2^(L-1).
    #    If s consists of only one '1' (i.e., "100...0"), then s == 2^(L-1), so T is not strictly less.
    
    L = len(s_binary)
    
    # Case 1: Trains with strictly fewer bits than s.
    # Train bit length = 2k + 1. We need 2k + 1 < L.
    # 2k < L - 1
    # k < (L - 1) / 2
    # Since k is integer >= 0, max k = floor((L - 2) / 2) if L >= 2, else no solution.
    # Number of values for k is floor((L - 2) / 2) + 1 if L >= 2, else 0.
    # Let's verify:
    # L=1: 2k < 0 -> impossible. Count = 0. Formula: (1-2)//2 + 1 = -1 + 1 = 0. Correct.
    # L=2: 2k < 1 -> k=0. Count = 1. Formula: (2-2)//2 + 1 = 0 + 1 = 1. Correct. (Train at 1, len=1 < 2)
    # L=3: 2k < 2 -> k=0. Count = 1. Formula: (3-2)//2 + 1 = 0 + 1 = 1. Correct. (Train at 1, len=1 < 3; train at 4 len=3 not < 3)
    # L=4: 2k < 3 -> k=0,1. Count = 2. Formula: (4-2)//2 + 1 = 1 + 1 = 2. Correct. (Trains at 1, 4; len 1,3 < 4)
    # L=5: 2k < 4 -> k=0,1. Count = 2. Formula: (5-2)//2 + 1 = 1 + 1 = 2. Correct. (Trains at 1, 4; len 1,3 < 5; train 16 len 5 not < 5)
    # L=6: 2k < 5 -> k=0,1,2. Count = 3. Formula: (6-2)//2 + 1 = 2 + 1 = 3. Correct.
    
    count = (L - 2) // 2 + 1 if L >= 1 else 0
    
    # Case 2: Train with same bit length as s.
    # Only possible if L is odd.
    if L % 2 == 1:
        # The train time would be 2^(L-1).
        # We need 2^(L-1) < s.
        # s is a binary string of length L starting with '1'.
        # s = 2^(L-1) + rest.
        # s > 2^(L-1) if and only if there is any '1' in s_other_than_first.
        if '1' in s_binary[1:]:
            count += 1
            
    print(count)

if __name__ == "__main__":
    solve()