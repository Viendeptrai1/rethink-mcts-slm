import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    V = int(data[1])
    
    max_volume = -1
    max_diff = -float('inf')
    
    index = 2
    for _ in range(n):
        l = int(data[index])
        w = int(data[index + 1])
        h = int(data[index + 2])
        
        volume = l * w * h
        
        if volume > max_volume:
            max_volume = volume
            max_diff = volume - V
        
        index += 3
    
    print(max_diff)

if __name__ == "__main__":
    main()