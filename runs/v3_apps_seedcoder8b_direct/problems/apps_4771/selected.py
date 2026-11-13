def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    n = int(data[0])
    V = int(data[1])
    
    max_difference = float('-inf')
    
    index = 2
    for _ in range(n):
        l = int(data[index])
        w = int(data[index + 1])
        h = int(data[index + 2])
        index += 3
        
        volume = l * w * h
        difference = volume - V
        
        if difference > max_difference:
            max_difference = difference
    
    print(max_difference)

if __name__ == "__main__":
    main()