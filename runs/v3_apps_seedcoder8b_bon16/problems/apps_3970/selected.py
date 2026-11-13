def largest_k_multiple_free_subset(n, k, numbers):
    numbers.sort()
    used = [False] * n
    count = 0

    for i in range(n):
        if used[i]:
            continue
        # Start a new subset with numbers[i]
        current = numbers[i]
        used[i] = True
        count += 1

        # Try to include as many multiples of current * k as possible
        for j in range(i + 1, n):
            if not used[j] and numbers[j] == current * k:
                used[j] = True

    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    n = int(data[0])
    k = int(data[1])
    numbers = list(map(int, data[2:]))
    
    result = largest_k_multiple_free_subset(n, k, numbers)
    print(result)

if __name__ == "__main__":
    main()