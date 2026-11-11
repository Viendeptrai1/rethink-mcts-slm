import sys

def solve(a, b, k):
    if k % 2 == 0:
        return (k // 2) * (a - b)
    else:
        return ((k // 2) * (a - b)) + a

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        k = int(data[index + 2])
        index += 3
        results.append(solve(a, b, k))
    
    print(' '.join(map(str, results)))

if __name__ == "__main__":
    main()