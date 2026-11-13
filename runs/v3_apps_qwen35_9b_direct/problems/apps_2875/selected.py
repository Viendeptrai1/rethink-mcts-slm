import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    v = [int(x) for x in input_data[1:]]

    # Create a sorted copy to compare
    sorted_v = sorted(v)

    # Find the first index where the arrays differ
    start = -1
    for i in range(n):
        if v[i] != sorted_v[i]:
            start = i
            break

    if start == -1:
        # Already sorted
        print("1 1")
        return

    # Find the last index where the arrays differ
    end = -1
    for i in range(n - 1, -1, -1):
        if v[i] != sorted_v[i]:
            end = i
            break

    # Check if reversing the subarray v[start:end+1] makes the array sorted
    # We simulate the reversal
    sub = v[start:end+1]
    sub.reverse()
    
    # Reconstruct the potential sorted array
    candidate = v[:start] + sub + v[end+1:]
    
    if candidate == sorted_v:
        print(f"{start + 1} {end + 1}")
    else:
        print("impossible")

if __name__ == "__main__":
    solve()