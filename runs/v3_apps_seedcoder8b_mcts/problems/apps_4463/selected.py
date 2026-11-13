def can_satisfy_lexicographic_order(s, t):
    from collections import Counter

    # Count the frequency of each character in both strings
    count_s = Counter(s)
    count_t = Counter(t)

    # Check if we can rearrange s to be lexicographically smaller than t
    for char in sorted(count_s.keys()):
        if count_s[char] < count_t[char]:
            return "Yes"
        elif count_s[char] > count_t[char]:
            return "No"

    # If all characters are the same in both strings, check their lengths
    if len(s) < len(t):
        return "Yes"
    else:
        return "No"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    s = data[0]
    t = data[1]
    print(can_satisfy_lexicographic_order(s, t))