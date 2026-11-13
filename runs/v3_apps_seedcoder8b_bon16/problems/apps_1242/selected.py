def lexicographically_smallest_prefix_reversal(s: str) -> None:
    result = []
    n = len(s)
    reversed_prefix = s[0]
    result.append(0)

    for i in range(1, n):
        if s[i] >= reversed_prefix[-1]:
            reversed_prefix += s[i]
            result.append(0)
        else:
            reversed_prefix = s[i] + reversed_prefix
            result.append(1)
    
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    lexicographically_smallest_prefix_reversal(input)