MOD = 998244353

def count_distinct_integers(N, X, A):
    # Convert X and all elements in A to integers
    X = int(X, 2)
    A = [int(a, 2) for a in A]
    
    # Set to store distinct integers
    distinct_integers = set(A)
    
    # Use a list to simulate the operations
    operations = list(distinct_integers)
    
    while operations:
        new_operations = []
        for x in operations:
            if 2 * x <= X:
                distinct_integers.add(2 * x)
                new_operations.append(2 * x)
            for y in operations:
                if x != y and x ^ y <= X:
                    distinct_integers.add(x ^ y)
                    new_operations.append(x ^ y)
        operations = new_operations
    
    return len(distinct_integers) % MOD

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
X = data[1]
A = data[2:N+2]

# Call the function and print the result
result = count_distinct_integers(N, X, A)
print(result)