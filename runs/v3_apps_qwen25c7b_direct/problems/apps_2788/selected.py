import sys

def max_students_to_lunch():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    group_sizes = list(map(int, data[1:n+1]))
    k = int(data[n+1])
    x = int(data[n+2])
    a = int(data[n+3])
    b = int(data[n+4])
    
    total_lunches_needed = sum(group_sizes)
    total_lunch_capacity = k * x
    
    if total_lunches_needed > total_lunch_capacity:
        return 'impossible'
    
    min_campers = a
    max_campers = b
    
    def can_take(num_students):
        if num_students < min_campers or num_students > max_campers:
            return False
        needed_bins = -(-num_students // x)  # Ceiling division
        return needed_bins <= k
    
    left, right = min_campers, max_campers + 1
    while left < right:
        mid = (left + right + 1) // 2
        if can_take(mid):
            left = mid
        else:
            right = mid - 1
    
    return left

if __name__ == "__main__":
    result = max_students_to_lunch()
    print(result)