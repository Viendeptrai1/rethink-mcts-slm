def add_elements(arr, k):
    """
    Given a non-empty array of integers arr and an integer k, return
    the sum of the elements with at most two digits from the first k elements of arr.
    """
    total = 0
    for i in range(k):
        num = arr[i]
        if abs(num) < 100:
            total += num
    return total