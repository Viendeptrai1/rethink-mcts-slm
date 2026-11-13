def find_longest_increasing_sequence(n, a):
    left, right = 0, n - 1
    result = []
    last = 0

    while left <= right:
        if a[left] > last:
            result.append('L')
            last = a[left]
            left += 1
        elif a[right] > last:
            result.append('R')
            last = a[right]
            right -= 1
        else:
            # If neither end can be added, we need to process the remaining elements
            if left < right:
                if a[left] < a[right]:
                    result.append('L')
                    last = a[left]
                    left += 1
                else:
                    result.append('R')
                    last = a[right]
                    right -= 1
            break

    print(len(result))
    print(''.join(result))

# Read input
n = int(input())
a = list(map(int, input().split()))

# Call the function
find_longest_increasing_sequence(n, a)