import sys
from collections import Counter

def max_rectangle_area(N, A):
    A.sort()
    count = Counter(A)
    max_area = 0
    
    for i in range(N-1, 2, -1):
        if count[A[i]] > 0:
            for j in range(i-1, 1, -1):
                if count[A[j]] > 0 and A[i] % A[j] == 0:
                    k = A[i] // A[j]
                    if k != A[j] and count[k] > 0:
                        max_area = max(max_area, A[j] * k)
    
    return max_area

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    A = list(map(int, data[1:]))
    print(max_rectangle_area(N, A))