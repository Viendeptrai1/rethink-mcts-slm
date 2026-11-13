import sys

def find_min_i(n, k):
    A = list(map(int, sys.stdin.readline().split()))
    current_sum = sum(A)
    i = 0
    
    while True:
        if any(num >= k for num in A):
            return i
        new_A = [sum(A[:j+1]) for j in range(n)]
        A = new_A
        current_sum += sum(new_A) - current_sum
        i += 1

if __name__ == "__main__":
    n, k = map(int, sys.stdin.readline().split())
    result = find_min_i(n, k)
    print(result)