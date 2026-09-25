import sys

def find_nice_indices(n, a):
    total_sum = sum(a)
    nice_indices = []

    for i in range(n):
        remaining_sum = total_sum - a[i]
        if remaining_sum % 2 == 0 and remaining_sum // 2 == a[i]:
            nice_indices.append(i + 1)

    return nice_indices

def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    a = list(map(int, data[1:]))

    nice_indices = find_nice_indices(n, a)

    print(len(nice_indices))
    if nice_indices:
        print(' '.join(map(str, nice_indices)))

if __name__ == "__main__":
    main()