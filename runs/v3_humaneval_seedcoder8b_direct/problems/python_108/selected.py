def count_nums(arr):
    def digit_sum(num):
        return sum(int(d) for d in str(abs(num)))
    
    return sum(1 for num in arr if digit_sum(num) > 0)