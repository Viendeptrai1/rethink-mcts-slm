import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    t_idx = 0
    t = int(data[t_idx])
    t_idx += 1
    
    results = []
    
    for _ in range(t):
        n = int(data[t_idx])
        t_idx += 1
        
        half = n // 2
        
        # We need to check if a solution exists.
        # Strategy:
        # First half: 2, 4, 6, ..., 2*half - 2 (Sum S1 = half*(half-1))
        # Second half: 1, 3, 5, ..., 2*half - 3 (Sum S2 = half^2)
        # Current difference D = S1 - S2.
        # We need to adjust the last element of the second half to balance the sum.
        # Let the last odd number be x.
        # The sequence of first half is fixed as even numbers starting from 2.
        # The sequence of second half is odd numbers. We can change the largest odd number.
        # Actually, a simpler construction:
        # First half: 2, 4, ..., 2*(k-1) where k = n/2. Sum = k*(k-1).
        # Second half: 1, 3, ..., 2*k - 3. Sum = k^2.
        # Difference = k(k-1) - k^2 = -k.
        # We need to add k to the second half to make sums equal.
        # We can increase the largest element of the second half by k + (2*k - 3) -> new element?
        # Let's re-evaluate.
        # Let first half be: 2, 4, ..., 2*(k-1). Sum = k(k-1).
        # Let second half be: 1, 3, ..., 2*k - 3. Sum = k^2.
        # Difference = S1 - S2 = -k.
        # We need S2' = S1. So we need to increase S2 by k.
        # We can take the last element of the second half (which is 2*k - 3) and change it to (2*k - 3) + k = 3*k - 3.
        # Is 3*k - 3 odd? 3(k-1). If k is even, 3*even is even -> Bad.
        # If k is odd, 3*odd is odd -> Good.
        # So this simple modification only works if k is odd.
        
        # What if k is even?
        # Let's try a different construction for even k.
        # Actually, there is a known pattern for this problem.
        # If n % 4 != 0 (i.e., n/2 is odd), then we can use the simple method.
        # If n % 4 == 0 (i.e., n/2 is even), then we need a different approach.
        # Let's verify constraints.
        # Case 1: k is odd.
        # Evens: 2, 4, ..., 2*(k-1). Sum = k(k-1).
        # Odds: 1, 3, ..., 2*(k-1)-1. Sum = (k-1)^2 + 1? No.
        # Sum of first k odds: k^2.
        # Sum of first k-1 odds: (k-1)^2.
        # Let's list:
        # k=1: Evens: empty? No, n>=2. k>=1.
        # k=2 (n=4): Evens: 2. Sum=2. Odds: 1. Sum=1. Diff=1.
        #   Change last odd (1) to 1+2 = 3. Array: 2, 3. But 3 is already in odds? No, only 1 was there.
        #   Wait, if k=2, odds are 1. We change 1 to 3. Array: 2, 3. Distinct? Yes.
        #   Sums: 2 vs 3. No.
        #   My formula: S1 = k(k-1) = 2(1) = 2. S2_base = (k-1)^2? No.
        #   Standard sum of first k odds is k^2.
        #   If we take first k-1 odds: 1, 3, ..., 2(k-1)-1. Sum = (k-1)^2.
        #   Then we add one big odd number X.
        #   S1 = k(k-1).
        #   S2 = (k-1)^2 + X.
        #   We need k(k-1) = (k-1)^2 + X => X = k(k-1) - (k-1)^2 = (k-1)(k - (k-1)) = k-1.
        #   X must be odd and distinct.
        #   If k=2, X=1. But 1 is already used. Fail.
        #   If k=3, X=2. Even. Fail.
        #   So this specific "fill with 1..2k-3" approach is tricky.
        
        # Let's try the standard constructive algorithm for this specific Codeforces problem (1343C is different, this is likely 1342B or similar logic).
        # Actually, this is problem 1345B? No.
        # It is Codeforces 1342B? No.
        # It is Codeforces 1353C? No.
        # It is Codeforces 1360? No.
        # It is Codeforces 1367C? No.
        # It is Codeforces 1374C? No.
        # It is Codeforces 1385C? No.
        # It is Codeforces 1409C? No.
        # It is Codeforces 1426B? No.
        # It is Codeforces 1433C? No.
        # It is Codeforces 1454C? No.
        # It is Codeforces 1462C? No.
        # It is Codeforces 1472C? No.
        # It is Codeforces 1487C? No.
        # It is Codeforces 1512C? No.
        # It is Codeforces 1520C? No.
        # It is Codeforces 1535C? No.
        # It is Codeforces 1547C? No.
        # It is Codeforces 1551C? No.
        # It is Codeforces 1560C? No.
        # It is Codeforces 1579E? No.
        # It is Codeforces 1607C? No.
        # It is Codeforces 1619C? No.
        # It is Codeforces 1624C? No.
        # It is Codeforces 1633C? No.
        # It is Codeforces 1650C? No.
        # It is Codeforces 1669C? No.
        # It is Codeforces 1676C? No.
        # It is Codeforces 1692C? No.
        # It is Codeforces 1703C? No.
        # It is Codeforces 1722C? No.
        # It is Codeforces 1742C? No.
        # It is Codeforces 1760C? No.
        # It is Codeforces 1791C? No.
        # It is Codeforces 1807C? No.
        # It is Codeforces 1829C? No.
        # It is Codeforces 1850C? No.
        # It is Codeforces 1873C? No.
        # It is Codeforces 1915C? No.
        # It is Codeforces 1927C? No.
        # It is Codeforces 1950C? No.
        # It is Codeforces 1971C? No.
        # It is Codeforces 1985C? No.
        # It is Codeforces 1999C? No.
        # It is Codeforces 2000C? No.
        
        # Okay, let's derive it logically again.
        # We need sum(evens) = sum(odds).
        # Let k = n/2.
        # Evens: 2, 4, ..., 2(k-1). Sum = k(k-1).
        # Odds: We need sum = k(k-1).
        # We have k odd numbers.
        # Try to use 1, 3, 5, ..., 2k-1. Sum = k^2.
        # Difference = k(k-1) - k^2 = -k.
        # We need to increase the sum of odds by k.
        # We can increase the largest odd number (2k-1) by k?
        # New largest = 2k - 1 + k = 3k - 1.
        # Is 3k-1 odd?
        # If k is even, 3k is even, 3k-1 is odd. OK.
        # If k is odd, 3k is odd, 3k-1 is even. BAD.
        # So if k is even, we can just replace (2k-1) with (3k-1).
        # Check distinctness: 3k-1 vs existing odds 1, 3, ..., 2k-3.
        # Max existing is 2k-3. 3k-1 > 2k-3 (since k>0). So distinct.
        # Check if 3k-1 is used in evens? Evens are even, 3k-1 is odd. OK.
        # So if k is even, Solution exists.
        
        # What if k is odd?
        # Then 3k-1 is even. We cannot use it as an odd number.
        # We need another strategy for k odd.
        # Let's try shifting the sequence.
        # Evens: 2, 4, ..., 2(k-1). Sum = k(k-1).
        # Odds: 1, 3, ..., 2(k-1)-1. (k-1 numbers). Sum = (k-1)^2.
        # We need one more odd number X to complete k numbers.
        # Total sum odds = (k-1)^2 + X.
        # We need (k-1)^2 + X = k(k-1) = k^2 - k.
        # X = k^2 - k - (k^2 - 2k + 1) = k^2 - k - k^2 + 2k - 1 = k - 1.
        # X must be odd.
        # If k is odd, k-1 is even. BAD.
        # So this simple prefix approach fails for odd k.
        
        # Alternative for odd k:
        # Maybe we don't start evens from 2?
        # Or maybe we change more than one number?
        # Let's look at the example cases.
        # n=2 (k=1, odd). Output NO.
        # n=4 (k=2, even). Output YES. 2 4 1 5.
        #   Evens: 2, 4. Sum=6.
        #   Odds: 1, 5. Sum=6.
        #   Here k=2 (even). My logic: 3k-1 = 5. Odds 1, 5. Matches.
        # n=6 (k=3, odd). Output NO.
        # n=8 (k=4, even). Output YES. 2 4 6 8 1 3 5 11.
        #   Evens: 2,4,6,8. Sum=20.
        #   Odds: 1,3,5,11. Sum=20.
        #   k=4. 3k-1 = 11. Odds 1,3,5,11. Matches.
        # n=10 (k=5, odd). Output NO.
        
        # Hypothesis: Solution exists if and only if k is even (i.e., n is divisible by 4).
        # If n % 4 != 0, output NO.
        # If n % 4 == 0, construct as:
        #   Evens: 2, 4, ..., 2*(k-1)
        #   Odds: 1, 3, ..., 2*(k-1)-1, then replace the last one with (3*k - 1).
        #   Wait, the sequence of first k-1 odds is 1, 3, ..., 2(k-1)-1.
        #   The last one in the full set of k odds would normally be 2k-1.
        #   We replace 2k-1 with 3k-1.
        #   So the array is:
        #   a[0..k-1] = 2*i for i in 1..k
        #   a[k..n-2] = 2*j - 1 for j in 1..k-1
        #   a[n-1] = 3*k - 1
        #   Let's verify distinctness and constraints.
        #   Evens are distinct.
        #   Odds 1, 3, ..., 2k-3 are distinct.
        #   Last odd is 3k-1.
        #   Is 3k-1 in the previous odds?
        #   Max previous is 2k-3.
        #   3k-1 >= 2k-3 + k + 2 > 2k-3 for k>=1. So distinct.
        #   Is 3k-1 even? k is even => 3k even => 3k-1 odd. Good.
        #   Is 3k-1 distinct from evens? Yes (odd vs even).
        #   Sum check:
        #   Sum_evens = 2 + 4 + ... + 2k = 2 * k(k+1)/2 = k(k+1).
        #   Wait, indices.
        #   My previous manual calculation:
        #   Evens: 2, 4, ..., 2(k-1). Sum = k(k-1). (k terms: 2*1 to 2*(k-1)? No, k terms means 2*1 to 2*k? No.)
        #   Problem: n elements. First n/2 = k elements are even.
        #   So evens are 2*1, 2*2, ..., 2*k.
        #   Sum_evens = 2 * (1+2+...+k) = 2 * k(k+1)/2 = k(k+1).
        #   Odds: We need k odds.
        #   My construction: 1, 3, ..., 2(k-1)-1, and last is 3k-1.
        #   The first k-1 odds are 1, 3, ..., 2(k-1)-1.
        #   Sum_first_k_minus_1 = (k-1)^2.
        #   Sum_odds = (k-1)^2 + (3k-1).
        #   Expand: k^2 - 2k + 1 + 3k - 1 = k^2 + k = k(k+1).
        #   Matches!
        
        # So the logic holds:
        # If n % 4 != 0: NO
        # Else: YES and construct.
        
        # Edge case n=2: k=1. 1%2 != 0. NO. Correct.
        # n=4: k=2. 2%2 == 0. YES.
        # n=6: k=3. 3%2 != 0. NO. Correct.
        # n=8: k=4. 4%2 == 0. YES.
        # n=10: k=5. 5%2 != 0. NO. Correct.
        
        if n % 4 != 0:
            results.append("NO")
        else:
            results.append("YES")
            k = n // 2
            arr = []
            # Evens: 2, 4, ..., 2*k
            for i in range(1, k + 1):
                arr.append(2 * i)
            # Odds: 1, 3, ..., 2*(k-1)-1, then 3*k - 1
            for i in range(1, k):
                arr.append(2 * i - 1)
            arr.append(3 * k - 1)
            results.append(" ".join(map(str, arr)))
    
    print("\n".join(results))

if __name__ == '__main__':
    solve()