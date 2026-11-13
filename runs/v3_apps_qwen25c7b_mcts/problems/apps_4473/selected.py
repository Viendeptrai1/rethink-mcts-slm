def frog_position(a, b, k):
    if k % 2 == 0:
        return 0
    else:
        if k == 1:
            return a
        elif k == 2:
            return a - b
        else:
            return a - b + a

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
        k = int(data[index + 2])
        index += 3
        
        result = frog_position(a, b, k)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()