def predict_moon_direction(n, a):
    if n == 1:
        return -1
    
    # Check if the sequence is strictly increasing or decreasing
    increasing = all(a[i] < a[i+1] for i in range(n-1))
    decreasing = all(a[i] > a[i+1] for i in range(n-1))
    
    if increasing:
        return "UP"
    elif decreasing:
        return "DOWN"
    else:
        # Determine the direction based on the last two days
        if a[-1] > a[-2]:
            return "UP"
        elif a[-1] < a[-2]:
            return "DOWN"
        else:
            return -1

# Example usage:
n = int(input())
a = list(map(int, input().split()))
print(predict_moon_direction(n, a))