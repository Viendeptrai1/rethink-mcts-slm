import sys

def count_rectangles(a, s):
    n = len(s)
    b = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            b[i][j] = int(s[i]) * int(s[j])
    
    count = 0
    
    for x in range(n):
        for y in range(x, n):
            for z in range(n):
                for t in range(z, n):
                    total = 0
                    for i in range(x, y + 1):
                        for j in range(z, t + 1):
                            total += b[i][j]
                    if total == a:
                        count += 1
    
    return count

if __name__ == "__main__":
    a = int(sys.stdin.readline().strip())
    s = sys.stdin.readline().strip()
    result = count_rectangles(a, s)
    print(result)