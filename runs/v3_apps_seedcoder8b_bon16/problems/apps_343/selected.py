def find_vova_marks(n, k, p, x, y, a):
    # Sort the existing marks to help calculate the median
    a.sort()

    # Calculate the current sum and median position
    current_sum = sum(a)
    median_position = (n + 1) // 2

    # Determine current median
    if k == 0:
        current_median = 1
    else:
        if k % 2 == 1:
            current_median = a[k // 2]
        else:
            current_median = a[k // 2 - 1]

    # Try to determine the required marks for remaining tests
    for i in range(n - k):
        # Try each possible mark from 1 to p
        for mark in range(1, p + 1):
            new_sum = current_sum + mark
            new_a = a + [mark]
            new_a.sort()

            # Determine new median
            if (k + i + 1) % 2 == 1:
                new_median = new_a[(k + i + 1) // 2]
            else:
                new_median = new_a[(k + i) // 2]

            # Check if new sum and median satisfy conditions
            if new_sum <= x and new_median >= y:
                a.append(mark)
                current_sum = new_sum
                break
        else:
            # If no mark works, return -1
            return [-1]

    # Return the remaining marks
    return a[k:]

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    n = int(data[0])
    k = int(data[1])
    p = int(data[2])
    x = int(data[3])
    y = int(data[4])
    a = list(map(int, data[5:5 + k]))
    
    result = find_vova_marks(n, k, p, x, y, a)
    
    if result == [-1]:
        print(result[0])
    else:
        print(" ".join(map(str, result)))