import sys
import math

def solve():
    q = int(input())
    for _ in range(q):
        k = int(input())
        
        # Find the block number
        block = 1
        while k > block * (block + 1) // 2:
            k -= block * (block + 1) // 2
            block += 1
        
        # Find the number within the block
        number = 1
        while k > len(str(number)):
            k -= len(str(number))
            number += 1
        
        # Find the digit within the number
        print(str(number)[k - 1])

if __name__ == "__main__":
    solve()