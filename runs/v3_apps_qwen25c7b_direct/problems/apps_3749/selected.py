import sys
from collections import defaultdict

MOD = 998244353

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    X = int(data[1], 2)
    
    A = [int(data[i+2], 2) for i in range(N)]
    
    # Initialize the set of numbers we can get
    possible_numbers = set(A)
    
    # Function to double a number
    def double(num):
        return num * 2
    
    # Function to compute XOR of two numbers
    def xor(num1, num2):
        return num1 ^ num2
    
    # Use BFS to explore all possible numbers
    queue = list(possible_numbers)
    while queue:
        current = queue.pop(0)
        if current > X:
            continue
        new_double = double(current)
        if new_double <= X and new_double not in possible_numbers:
            possible_numbers.add(new_double)
            queue.append(new_double)
        for other in possible_numbers:
            new_xor = xor(current, other)
            if new_xor <= X and new_xor not in possible_numbers:
                possible_numbers.add(new_xor)
                queue.append(new_xor)
    
    # Count the number of unique numbers not exceeding X
    result = len([num for num in possible_numbers if num <= X])
    
    print(result % MOD)

if __name__ == "__main__":
    main()