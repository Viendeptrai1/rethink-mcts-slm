from collections import deque

def count_reachable_integers(N, X, A):
    MOD = 998244353
    X = int(X, 2)
    A = [int(a, 2) for a in A]
    
    reachable = set(A)
    queue = deque(A)
    
    while queue:
        current = queue.popleft()
        
        # Double the current number
        doubled = current * 2
        if doubled <= X and doubled not in reachable:
            reachable.add(doubled)
            queue.append(doubled)
        
        # XOR with each number in A
        for num in A:
            xor_result = current ^ num
            if xor_result <= X and xor_result not in reachable:
                reachable.add(xor_result)
                queue.append(xor_result)
    
    # Count numbers not exceeding X
    count = sum(1 for num in reachable if num <= X)
    return count % MOD

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
X = data[1]
A = data[2:]

# Calculate and print the result
result = count_reachable_integers(N, X, A)
print(result)