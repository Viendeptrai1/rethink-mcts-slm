import sys

def min_operations(a, b, c):
    # Ensure B is divisible by A
    if b % a != 0:
        ops = b % a
        a += ops
        b += ops
    else:
        ops = 0
    
    # Ensure C is divisible by B
    if c % b != 0:
        ops += c % b
        b += c % b
        c += c % b
    
    return ops, a, b, c

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
        c = int(data[index + 2])
        index += 3
        
        ops, A, B, C = min_operations(a, b, c)
        results.append((ops, A, B, C))
    
    for res in results:
        print(res[0])
        print(res[1], res[2], res[3])

if __name__ == "__main__":
    main()