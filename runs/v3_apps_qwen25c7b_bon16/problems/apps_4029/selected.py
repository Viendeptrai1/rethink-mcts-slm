def min_moves_to_divisible_by_25(n):
    s = str(n)
    if int(s[-1]) == 0 and int(s[-2]) == 0:
        return 0
    elif (int(s[-1]) == 5 or int(s[-1]) == 0) and '0' in s[:-1]:
        pos_zero = s.rfind('0')
        if int(s[-1]) == 5:
            return abs(pos_zero - len(s) + 1)
        else:
            return abs(pos_zero - len(s))
    elif int(s[-2:]) % 25 == 0:
        return 0
    else:
        for i in range(len(s) - 2):
            for j in range(i + 1, len(s)):
                if int(s[j] + s[i]) % 25 == 0:
                    return j - i
        return -1

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    result = min_moves_to_divisible_by_25(n)
    print(result)