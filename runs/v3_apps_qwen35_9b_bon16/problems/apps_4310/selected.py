import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    A = list(map(int, data))
    if len(A) == 1:
        print(0)
        return
    if len(A) == 2:
        print(abs(A[1] - A[0]))
        return

    A.sort()
    # Optimal strategy for n=3 is to go from min to max directly in two steps
    # Cost = (max - mid) + (mid - min) = max - min
    # But we can also do min -> mid -> max or any permutation starting with cost 0 on first
    # Actually for 3 sorted values a <= b <= c:
    # Option 1: a -> b -> c : cost 0 + (b-a) + (c-b) = c - a
    # Option 2: a -> c -> b : cost 0 + (c-a) + |b-c| = (c-a) + (c-b) = 2c - a - b
    # Option 3: b -> a -> c : cost 0 + (b-a) + (c-a) = b - a + c - a = b + c - 2a
    # Option 4: b -> c -> a : cost 0 + (c-b) + (c-a) = c - b + c - a = 2c - a - b
    # Option 5: c -> a -> b : cost 0 + (c-a) + (b-a) = c - a + b - a = b + c - 2a
    # Option 6: c -> b -> a : cost 0 + (c-b) + (b-a) = c - a
    # Minimum is min(c-a, 2c-a-b, b+c-2a)
    # For sorted a<=b<=c, c-a is always <= b+c-2a because b>=a => b-a>=0 => b+c-2a = (c-a)+(b-a) >= c-a
    # Similarly, c-a <= 2c-a-b because 2c-a-b - (c-a) = c-b >=0
    # So minimum is c-a
    print(A[-1] - A[0])

if __name__ == "__main__":
    solve()