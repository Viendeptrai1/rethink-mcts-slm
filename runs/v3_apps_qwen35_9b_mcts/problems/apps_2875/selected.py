import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        v = []
        for _ in range(n):
            v.append(int(next(iterator)))
    except StopIteration:
        return

    # Create a sorted copy to compare against
    sorted_v = sorted(v)

    # Find the first index where the array differs from the sorted version
    start = -1
    for i in range(n):
        if v[i] != sorted_v[i]:
            start = i
            break

    # If no differences, the array is already sorted
    if start == -1:
        print("1 1")
        return

    # Find the last index where the array differs from the sorted version
    end = -1
    for i in range(n - 1, -1, -1):
        if v[i] != sorted_v[i]:
            end = i
            break

    # The candidate segment to reverse is from start to end (inclusive, 0-based)
    # We need to check if reversing v[start:end+1] makes the array equal to sorted_v
    # This is equivalent to checking if v[start:end+1] is the reverse of sorted_v[start:end+1]

    segment = v[start:end+1]
    reversed_segment = segment[::-1]

    if reversed_segment == sorted_v[start:end+1]:
        # Convert to 1-based indexing for output
        print(f"{start + 1} {end + 1}")
    else:
        print("impossible")

if __name__ == "__main__":
    solve()