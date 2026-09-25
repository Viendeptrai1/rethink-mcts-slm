def add_elements(arr, k):
    total_sum = 0
    for i in range(k):
        if -99 <= arr[i] <= 99:
            total_sum += arr[i]
    return total_sum