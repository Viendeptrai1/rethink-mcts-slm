def can_take_students(students, k, x, a, b, mid):
    total_lunches_needed = (mid + x - 1) // x
    total_lunches_available = k * x
    total_students = sum(students)
    
    if total_students < mid:
        return False
    
    if total_lunches_needed <= total_lunches_available:
        return True
    
    return False

def max_students_to_lunch(n, sizes, k, x, a, b):
    left, right = a, min(b, sum(sizes))
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if can_take_students(sizes, k, x, a, b, mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return result if result != -1 else "impossible"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    sizes = list(map(int, data[1:n+1]))
    k, x, a, b = map(int, data[n+1:n+5])
    
    result = max_students_to_lunch(n, sizes, k, x, a, b)
    print(result)

if __name__ == "__main__":
    main()