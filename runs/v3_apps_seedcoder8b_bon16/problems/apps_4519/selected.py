def lexicographically_minimum_string(n, k, s):
    s = list(s)
    for i in range(n):
        if k == 0:
            break
        min_index = i
        # Look for the minimum character in the range we can reach
        for j in range(i + 1, min(n, i + k + 1)):
            if s[j] < s[min_index]:
                min_index = j
        # Calculate the number of moves needed to bring min_index to position i
        moves_needed = min_index - i
        # Move the minimum character to the current position
        if min_index != i:
            for j in range(min_index, i, -1):
                s[j], s[j - 1] = s[j - 1], s[j]
            k -= moves_needed
    return ''.join(s)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    q = int(data[index])
    index += 1
    results = []
    
    for _ in range(q):
        n = int(data[index])
        k = int(data[index + 1])
        s = data[index + 2]
        index += 3
        result = lexicographically_minimum_string(n, k, s)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()