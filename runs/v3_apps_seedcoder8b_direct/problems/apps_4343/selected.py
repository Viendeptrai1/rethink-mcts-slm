def find_median_string(k, s, t):
    def count_strings_less_equal(x):
        count = 0
        for i in range(k):
            if x[i] < s[i]:
                return count
            elif x[i] > t[i]:
                return count
            count += ord(x[i]) - ord('a') + 1
        return count

    def find_median():
        low = s
        high = t
        while low != high:
            mid = [((ord(l) + ord(h)) // 2) for l, h in zip(low, high)]
            mid = [chr(m) for m in mid]
            mid_str = ''.join(mid)
            if count_strings_less_equal(mid_str) < (total_strings + 1) // 2:
                low = [chr(ord(m) + 1) for m in mid]
                low = ''.join(low)
            else:
                high = mid_str
        return low

    total_strings = count_strings_less_equal(t) - count_strings_less_equal(s) + 1
    return find_median()

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    k = int(data[0])
    s = data[1]
    t = data[2]
    print(find_median_string(k, s, t))