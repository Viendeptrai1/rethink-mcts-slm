import sys

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
        
        remainder = a % b
        if remainder == 0:
            results.append(0)
        else:
            results.append(b - remainder)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()