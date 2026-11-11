import sys

def min_insertions_to_avoid_zero_sum_subarray(n, a):
    prefix_sums = set()
    current_sum = 0
    insertions = 0

    for i in range(n):
        current_sum += a[i]
        if current_sum in prefix_sums:
            insertions += 1
            prefix_sums.clear()
            current_sum = a[i]
        prefix_sums.add(current_sum)

    return insertions

def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    a = list(map(int, data[1:]))

    result = min_insertions_to_avoid_zero_sum_subarray(n, a)
    print(result)

if __name__ == "__main__":
    main()