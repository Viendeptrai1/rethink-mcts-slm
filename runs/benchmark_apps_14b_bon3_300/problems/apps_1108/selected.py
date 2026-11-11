import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    index = 1
    count = 0
    
    for _ in range(n):
        pi = int(data[index])
        qi = int(data[index + 1])
        if qi - pi >= 2:
            count += 1
        index += 2
    
    print(count)

if __name__ == "__main__":
    main()