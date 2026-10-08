import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    V = int(data[1])
    
    max_volume = -1
    for i in range(n):
        l = int(data[2 + 3 * i])
        w = int(data[3 + 3 * i])
        h = int(data[4 + 3 * i])
        volume = l * w * h
        if volume > max_volume:
            max_volume = volume
    
    d = max_volume - V
    print(d)

if __name__ == "__main__":
    main()