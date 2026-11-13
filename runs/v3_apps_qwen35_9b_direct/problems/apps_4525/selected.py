import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    t = int(data[idx])
    idx += 1
    
    results = []
    
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        
        half = n // 2
        
        # Calculate sum of first half: 2, 4, ..., 2*half
        # Sum = 2 * (1 + 2 + ... + half) = 2 * (half * (half + 1) // 2) = half * (half + 1)
        sum_first = half * (half + 1)
        
        # We need sum of second half to be equal to sum_first.
        # Second half elements are odd: 1, 3, 5, ..., 2*half-1
        # Sum of first half of odds (1 to 2*half-1) = half^2
        current_sum_odds = half * half
        diff = sum_first - current_sum_odds
        
        # If diff is even and positive, we can add diff/2 to the last odd number
        # because adding an even number to an odd number keeps it odd.
        # Also, we must ensure the modified last number doesn't collide with any even number.
        # Even numbers are up to 2*half.
        # The last odd number before modification is 2*half - 1.
        # Modified last odd = 2*half - 1 + diff.
        # Since diff = sum_first - half^2 = half(half+1) - half^2 = half.
        # So diff is always half.
        # Modified last odd = 2*half - 1 + half = 3*half - 1.
        # We need 3*half - 1 > 2*half (to be distinct from evens) => half > 1 => n > 2.
        # Also diff must be even? No, diff is half. We add diff to the last odd.
        # Wait, logic check:
        # Sum required = S.
        # Sum of 1, 3, ..., 2*half-1 is half^2.
        # We need to increase the sum by (S - half^2).
        # S - half^2 = half(half+1) - half^2 = half.
        # So we need to add 'half' to the sum of the odd numbers.
        # We can add this 'half' to the last element of the odd sequence.
        # Last element becomes (2*half - 1) + half = 3*half - 1.
        # Is 3*half - 1 odd?
        # If half is even, 3*even - 1 = even - 1 = odd. OK.
        # If half is odd, 3*odd - 1 = odd - 1 = even. NOT OK.
        # So if half is odd, the last element becomes even, which violates the condition.
        # Therefore, a solution exists if and only if half is even.
        # half = n/2. So n/2 must be even => n must be divisible by 4.
        
        if half % 2 != 0:
            results.append("NO")
        else:
            results.append("YES")
            # Construct array
            evens = []
            for i in range(1, half + 1):
                evens.append(2 * i)
            
            odds = []
            for i in range(1, half + 1):
                val = 2 * i - 1
                if i == half:
                    val += half
                odds.append(val)
            
            res_arr = evens + odds
            results.append(" ".join(map(str, res_arr)))
    
    print("\n".join(results))

if __name__ == "__main__":
    solve()