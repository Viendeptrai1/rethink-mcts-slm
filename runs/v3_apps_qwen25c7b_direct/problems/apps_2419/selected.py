def min_operations(a, b):
    return abs(a - b)

def main():
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
        results.append(min_operations(a, b))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()