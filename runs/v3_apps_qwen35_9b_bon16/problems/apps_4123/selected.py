import sys

def solve():
    try:
        input = sys.stdin.read().split()
    except Exception:
        return

    if not input:
        return

    n = int(input[0])
    s = input[1]

    from collections import Counter

    two_grams = []
    for i in range(n - 1):
        two_grams.append(s[i:i+2])

    if not two_grams:
        return

    counter = Counter(two_grams)
    most_frequent = max(counter, key=counter.get)
    print(most_frequent)

if __name__ == "__main__":
    solve()