import sys

def find_nice_indices(n, a):
    total_sum = sum(a)
    prefix_sum = [0] * n
    nice_indices = []

    for i in range(1, n):
        prefix_sum[i] = prefix_sum[i - 1] + a[i - 1]

    for j in range(n):
        left_sum = prefix_sum[j]
        right_sum = total_sum - prefix_sum[j] - a[j]
        if a[j] == left_sum + right_sum:
            nice_indices.append(j + 1)

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