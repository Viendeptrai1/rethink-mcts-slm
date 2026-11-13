def max_students_for_lunch(n, sizes, k, x, a, b):
    # Calculate the total number of students
    total_students = sum(sizes)
    
    # Calculate the total lunches available
    total_lunches = k * x
    
    # If total students are more than total lunches, it's impossible
    if total_students > total_lunches:
        return "impossible"
    
    # Initialize binary search bounds
    left, right = a, min(total_students, b)
    
    # Function to check if a given number of students is feasible
    def can_feed(students):
        # Check if students are within the safe viewing range
        if students < a or students > b:
            return False
        
        # Check if we have enough groups to serve those students
        current_students = 0
        groups_served = 0
        for size in sorted(sizes, reverse=True):
            if current_students + size <= students:
                current_students += size
                groups_served += 1
                if current_students == students:
                    return True
        
        return False
    
    # Perform binary search to find the maximum feasible number of students
    result = "impossible"
    while left <= right:
        mid = (left + right) // 2
        if can_feed(mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return result

# Read input
n = int(input().strip())
sizes = list(map(int, input().strip().split()))
k, x, a, b = map(int, input().strip().split())

# Compute and print the result
print(max_students_for_lunch(n, sizes, k, x, a, b))