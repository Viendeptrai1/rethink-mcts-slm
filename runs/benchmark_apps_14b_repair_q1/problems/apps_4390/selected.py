def min_moves_to_divisible(a, b):
    return (b - (a % b)) % b

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
        b = int(data[index + 1])
        index += 2
        results.append(min_moves_to_divisible(a, b))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()