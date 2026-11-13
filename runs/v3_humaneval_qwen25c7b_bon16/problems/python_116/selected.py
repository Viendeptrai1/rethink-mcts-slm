def count_ones(num):
    return bin(num).count('1')

def sort_array(arr):
    return sorted(arr, key=lambda x: (count_ones(x), x))