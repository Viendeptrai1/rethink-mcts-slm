import sys

def min_rest_days(n, activities):
    memo = {}

    def dp(day, last_activity):
        if day == n:
            return 0
        if (day, last_activity) in memo:
            return memo[(day, last_activity)]

        rest = dp(day + 1, -1) + 1
        if activities[day] == 0:
            pass
        elif activities[day] == 1:
            if last_activity != 1:
                rest = min(rest, dp(day + 1, 1))
        elif activities[day] == 2:
            if last_activity != 2:
                rest = min(rest, dp(day + 1, 2))
        elif activities[day] == 3:
            if last_activity != 1:
                rest = min(rest, dp(day + 1, 1))
            if last_activity != 2:
                rest = min(rest, dp(day + 1, 2))

        memo[(day, last_activity)] = rest
        return rest

    return dp(0, -1)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    activities = list(map(int, data[1:]))
    print(min_rest_days(n, activities))

if __name__ == "__main__":
    main()