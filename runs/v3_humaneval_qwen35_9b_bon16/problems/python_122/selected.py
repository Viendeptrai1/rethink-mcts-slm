def add_elements(arr, k):
    total = 0
    for i in range(k):
        num = arr[i]
        if 0 <= num <= 99:
            total += num
    return total