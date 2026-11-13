import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))

    a = []
    for _ in range(n):
        a.append(int(next(iterator)))

    # We need to find the starting index (1-based) that minimizes the sum of every k-th element
    # in the cyclic sequence starting from that index.
    # Since n is divisible by k, there are exactly n/k such elements for any starting position.
    # The elements picked for a start index i (0-based) are:
    # i, (i+k)%n, (i+2k)%n, ..., (i+(n/k - 1)*k)%n
    # Notice that these indices are all congruent to i modulo k.
    # Therefore, we can simply sum the elements at indices j where j % k == r for each remainder r from 0 to k-1.
    # The starting task number corresponding to remainder r is r + 1.

    min_total_power = float('inf')
    best_start = -1

    # There are k possible remainders (0 to k-1)
    for r in range(k):
        current_sum = 0
        # Sum all elements a[j] where j % k == r
        # We can iterate through the array once or step by k. Since n <= 10^5, stepping is efficient.
        # However, to be safe and clear, we iterate j from r to n-1 with step k.
        for j in range(r, n, k):
            current_sum += a[j]
        
        if current_sum < min_total_power:
            min_total_power = current_sum
            best_start = r + 1
        # If equal, we want the minimum start number. Since we iterate r from 0 upwards,
        # the first time we see the minimum is the smallest start number. So we don't update on equality.

    print(best_start)

if __name__ == '__main__':
    solve()