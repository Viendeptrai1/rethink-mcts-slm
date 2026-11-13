def predict_moon_phase(n, a):
    if n == 1:
        return -1
    if a[n-1] < a[n-2]:
        return "UP"
    elif a[n-1] > a[n-2]:
        return "DOWN"
    else:
        return -1

# Example usage:
# n = int(input())
# a = list(map(int, input().split()))
# result = predict_moon_phase(n, a)
# print(result)