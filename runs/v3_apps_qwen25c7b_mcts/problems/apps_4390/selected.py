def min_moves_to_divisible(a, b):
    return (b - a % b) % b

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    index = 1
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        index += 2
        results.append(min_moves_to_divisible(a, b))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    solve()