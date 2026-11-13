def solve():
    s = input().strip()
    t = input().strip()

    # Count the frequency of each character in s and t
    s_count = [0] * 26
    t_count = [0] * 26

    for char in s:
        s_count[ord(char) - ord('a')] += 1

    for char in t:
        t_count[ord(char) - ord('a')] += 1

    # Check if s' < t' is possible
    for i in range(26):
        if s_count[i] < t_count[i]:
            print("Yes")
            return
        elif s_count[i] > t_count[i]:
            print("No")
            return

    # If we reach here, s and t are identical
    print("No")

solve()