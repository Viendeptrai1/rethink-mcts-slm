import sys

def count_rectangles(a, s):
    n = len(s)
    prefix_sum = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            prefix_sum[i][j] = prefix_sum[i - 1][j] + prefix_sum[i][j - 1] - prefix_sum[i - 1][j - 1] + int(s[i - 1]) * int(s[j - 1])
    
    count = 0
    for x in range(1, n + 1):
        for y in range(x, n + 1):
            for z in range(1, n + 1):
                for t in range(z, n + 1):
                    if prefix_sum[y][t] - prefix_sum[x - 1][t] - prefix_sum[y][z - 1] + prefix_sum[x - 1][z - 1] == a:
                        count += 1
    
    return count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    a = int(data[0])
    s = data[1]
    result = count_rectangles(a, s)
    print(result)