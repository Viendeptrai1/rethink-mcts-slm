import sys

def max_good_sleeping_times(n, h, l, r, a):
    def is_good_time(time):
        return l <= time % h <= r

    def dp(i, current_time):
        if i == n:
            return 0
        # Option 1: Sleep after a[i] hours
        option1 = dp(i + 1, (current_time + a[i]) % h)
        # Option 2: Sleep after a[i] - 1 hours
        option2 = dp(i + 1, (current_time + a[i] - 1) % h)
        # Choose the best option
        return max(option1, option2 + int(is_good_time((current_time + a[i] - 1) % h)))

    return dp(0, 0)

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
h = int(data[1])
l = int(data[2])
r = int(data[3])
a = list(map(int, data[4:]))

# Calculate and print the result
result = max_good_sleeping_times(n, h, l, r, a)
print(result)