def max_happiness(n, m, moods, subarrays):
    # Initialize a list to count the number of subarrays each flower is in
    flower_count = [0] * n

    # Iterate over each subarray and mark the flowers it contains
    for l, r in subarrays:
        for i in range(l - 1, r):
            flower_count[i] += 1

    # Calculate the total happiness
    total_happiness = 0
    for i in range(n):
        total_happiness += moods[i] * flower_count[i]

    return total_happiness

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    moods = list(map(int, data[2:n+2]))
    subarrays = []
    
    index = n + 2
    for _ in range(m):
        l = int(data[index])
        r = int(data[index + 1])
        subarrays.append((l, r))
        index += 2
    
    result = max_happiness(n, m, moods, subarrays)
    print(result)

if __name__ == "__main__":
    main()