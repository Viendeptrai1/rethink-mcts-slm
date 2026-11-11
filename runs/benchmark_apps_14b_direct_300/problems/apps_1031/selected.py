import sys

def paint_cardiogram(n, a):
    total_length = sum(a)
    max_height = max(sum(a[:i+1]) for i in range(0, n, 2)) - min(sum(a[:i+1]) for i in range(1, n, 2))
    
    for y in range(max_height, -max_height-1, -1):
        line = [' '] * total_length
        x = 0
        for i in range(n):
            if i % 2 == 0:
                if y <= sum(a[:i+1]) and y > sum(a[:i]):
                    line[x] = '/'
            else:
                if y <= sum(a[:i+1]) and y > sum(a[:i]):
                    line[x] = '\\'
            x += a[i]
        print(''.join(line))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    paint_cardiogram(n, a)

if __name__ == "__main__":
    main()