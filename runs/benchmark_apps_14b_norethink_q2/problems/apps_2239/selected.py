import sys

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    index = 1
    for _ in range(t):
        x = int(data[index])
        index += 1
        
        # The minimum sum of two dice rolls is 4 (2+2)
        # If x is divisible by 4, then we can achieve x with x//4 rolls
        if x % 4 == 0:
            results.append(x // 4)
        else:
            # Otherwise, we need at least one more roll to adjust the sum
            results.append((x + 3) // 4)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    solve()