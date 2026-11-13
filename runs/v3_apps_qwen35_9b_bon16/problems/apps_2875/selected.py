import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    v = [int(x) for x in input_data[1:]]

    if n == 1:
        print("1 1")
        return

    # Create a sorted version of the array
    sorted_v = sorted(v)

    # Find the first index where v differs from sorted_v
    start = -1
    for i in range(n):
        if v[i] != sorted_v[i]:
            start = i
            break

    if start == -1:
        # Already sorted
        print("1 1")
        return

    # Find the last index where v differs from sorted_v
    end = -1
    for i in range(n - 1, -1, -1):
        if v[i] != sorted_v[i]:
            end = i
            break

    # If no differences found in reverse (shouldn't happen if start != -1), but safety check
    if end == -1:
        print("1 1")
        return

    # Extract the subarray to reverse
    subarray = v[start:end+1]
    reversed_subarray = subarray[::-1]

    # Construct the candidate array
    candidate = v[:start] + reversed_subarray + v[end+1:]

    # Check if candidate is sorted
    if candidate == sorted_v:
        # Output 1-based indices
        print(f"{start + 1} {end + 1}")
    else:
        print("impossible")

if __name__ == "__main__":
    solve()