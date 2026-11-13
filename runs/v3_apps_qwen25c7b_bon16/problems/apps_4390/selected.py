def min_moves_to_divisible(a, b):
    return (b - (a % b)) % b

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
        
        result = min_moves_to_divisible(a, b)
        results.append(str(result))
    
    print('\n'.join(results))

if __name__ == "__main__":
    main()