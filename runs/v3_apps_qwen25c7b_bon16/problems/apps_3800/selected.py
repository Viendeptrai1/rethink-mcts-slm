from typing import List

def count_rectangles(a: int, s: str) -> int:
    n = len(s)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    count = 0
    
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            for k in range(1, n + 1):
                for l in range(k, n + 1):
                    submatrix_sum = sum(int(s[m-1]) * int(s[n-1]) for m in range(i, j+1) for n in range(k, l+1))
                    if submatrix_sum == a:
                        count += 1
    
    return count

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    a = int(data[0])
    s = data[1]
    result = count_rectangles(a, s)
    print(result)