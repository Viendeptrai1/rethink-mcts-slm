import sys
input = sys.stdin.read
data = input().split()

X = int(data[0])
K = int(data[1])
D = int(data[2])

# Calculate the remainder when K is divided by 2
remainder = K % 2

# If the remainder is 0, the minimum absolute value is the remainder of X divided by D
if remainder == 0:
    min_abs_value = abs(X) % D
else:
    # If the remainder is 1, we need to consider moving closer to zero
    if abs(X) >= D:
        min_abs_value = abs(X) - D
    else:
        min_abs_value = abs(X)

print(min_abs_value)