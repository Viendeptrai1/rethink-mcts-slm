def find_median_string(k, s, t):
    def count_strings(prefix):
        if len(prefix) == k:
            return 1
        count = 0
        for c in range(ord('a'), ord('z') + 1):
            if chr(c) >= s[len(prefix)] and chr(c) <= t[len(prefix)]:
                count += count_strings(prefix + chr(c))
        return count

    def find_median(prefix, target_index):
        if len(prefix) == k:
            return prefix
        for c in range(ord('a'), ord('z') + 1):
            if chr(c) >= s[len(prefix)] and chr(c) <= t[len(prefix)]:
                count = count_strings(prefix + chr(c))
                if target_index < count:
                    return find_median(prefix + chr(c), target_index)
                target_index -= count
        return ""

    total_count = count_strings("")
    median_index = (total_count - 1) // 2
    return find_median("", median_index)

k = int(input())
s = input().strip()
t = input().strip()
result = find_median_string(k, s, t)
print(result)