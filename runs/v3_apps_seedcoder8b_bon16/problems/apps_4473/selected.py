def calculate_frog_position(t, queries):
    results = []
    for query in queries:
        a, b, k = query
        # Calculate the net displacement in one cycle of jumps
        cycle_displacement = a - b
        # Determine the net effect over k jumps
        net_displacement = cycle_displacement * (k // 2)
        # Adjust if there is an odd number of jumps in the cycle
        if k % 2 == 1:
            net_displacement += a
        # Append the result for this query
        results.append(net_displacement)
    return results

import sys

def main():
    input = sys.stdin.read
    data = input().split()
    t = int(data[0])
    queries = []
    index = 1
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        k = int(data[index + 2])
        queries.append((a, b, k))
        index += 3
    results = calculate_frog_position(t, queries)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()