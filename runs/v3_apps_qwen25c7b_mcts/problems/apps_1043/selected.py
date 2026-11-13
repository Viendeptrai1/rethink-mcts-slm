def min_bribes(n, a):
    friend_index = a.index(-1)
    total_cost = 0
    
    while n > 1:
        # Calculate the number of rounds needed
        rounds = n.bit_length() - 1
        
        # Iterate over each round
        for _ in range(rounds):
            # Identify the matches involving the friend boxer
            for i in range(0, n, 2):
                if i // 2 == friend_index or (i + 1) // 2 == friend_index:
                    if a[i] != -1 and a[i + 1] != -1:
                        # Bribe the weaker opponent
                        if a[i] < a[i + 1]:
                            total_cost += a[i]
                            a[i] = -1
                        else:
                            total_cost += a[i + 1]
                            a[i + 1] = -1
                    elif a[i] != -1:
                        total_cost += a[i]
                        a[i] = -1
                    elif a[i + 1] != -1:
                        total_cost += a[i + 1]
                        a[i + 1] = -1
        
        # Halve the number of boxers for the next round
        n //= 2
    
    return total_cost

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

print(min_bribes(n, a))