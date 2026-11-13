def max_juice(n, moves):
    max_drunk = 0
    for i in range(n):
        count = 0
        for j in range(i, len(moves), n):
            if j >= 3 and moves[j] == moves[j-1] == moves[j-2]:
                count += 1
            else:
                break
        max_drunk = max(max_drunk, count)
    return max_drunk

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    moves = data[1]
    result = max_juice(n, moves)
    print(result)