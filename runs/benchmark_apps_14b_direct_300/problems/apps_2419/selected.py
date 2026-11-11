import sys

def min_operations(a, b):
    if a == b:
        return 0
    diff = abs(b - a)
    n = int((diff * 2)**0.5)
    while n * (n + 1) // 2 < diff:
        n += 1
    if n * (n + 1) // 2 >= diff:
        return n
    else:
        return n + 1

def main():
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
        results.append(min_operations(a, b))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()