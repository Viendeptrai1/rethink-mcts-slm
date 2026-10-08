import sys

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
        
        net_effect = (k // 2) * (a - b)
        if k % 2 == 1:
            net_effect += a
        
        results.append(net_effect)
    
    print(' '.join(map(str, results)))

if __name__ == "__main__":
    main()