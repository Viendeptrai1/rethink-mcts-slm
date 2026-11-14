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
        
        if n % 4 != 0:
            results.append("NO")
        else:
            results.append("YES")
            half = n // 2
            
            # First half: even numbers 2, 4, ..., n
            evens = list(range(2, n + 1, 2))
            
            # Second half: odd numbers 1, 3, ..., n-1
            odds = list(range(1, n, 2))
            
            # Calculate sums
            sum_evens = sum(evens)
            sum_odds = sum(odds)
            
            # Difference
            diff = sum_evens - sum_odds
            
            # We need to add diff to the sum of odds to match sum_evens
            # Since diff is even (sum_evens is even, sum_odds is even because n/2 is even),
            # we can add diff to the last odd number.
            # The last odd number is n-1.
            # New last odd number = (n-1) + diff
            # Check constraints: (n-1) + diff <= 10^9?
            # Max n = 2*10^5, sum_evens approx n^2/4, sum_odds approx n^2/4.
            # diff is roughly n^2/4 - n^2/4 = 0? No.
            # Sum evens = 2 + 4 + ... + n = 2 * (1 + ... + n/2) = 2 * (n/2)*(n/2+1)/2 = (n/2)*(n/2+1)
            # Sum odds = 1 + 3 + ... + (n-1) = (n/2)^2
            # diff = (n/2)*(n/2+1) - (n/2)^2 = (n/2)^2 + n/2 - (n/2)^2 = n/2
            # So diff = n/2.
            # New last odd = (n-1) + n/2 = 1.5n - 1.
            # For n=2*10^5, 1.5n = 3*10^5, well within 10^9.
            
            offset = diff
            odds[-1] += offset
            
            # Construct the array
            a = evens + odds
            results.append(" ".join(map(str, a)))
    
    print("\n".join(results))

if __name__ == "__main__":
    solve()