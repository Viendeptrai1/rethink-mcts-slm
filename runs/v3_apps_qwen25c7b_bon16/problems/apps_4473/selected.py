def frog_position(a, b, k):
    return a * (k // 2) - b * (k // 2) + (a if k % 2 != 0 else 0)

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    
    results = []
    for _ in range(t):
        a = int(data[index])
        index += 1
        b = int(data[index])
        index += 1
        k = int(data[index])
        index += 1
        
        result = frog_position(a, b, k)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    solve()