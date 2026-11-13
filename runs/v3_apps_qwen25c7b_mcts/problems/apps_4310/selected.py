import sys

def min_cost_to_complete_tasks():
    A = list(map(int, sys.stdin.readline().split()))
    A.sort()
    return abs(A[1] - A[0]) + abs(A[2] - A[1])

if __name__ == "__main__":
    print(min_cost_to_complete_tasks())