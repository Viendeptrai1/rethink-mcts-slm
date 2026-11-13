def max_skill_sum(n, a, b):
    # Create a list of tuples (a_i, b_i) for each student
    students = list(zip(a, b))
    
    # Sort students by skill level in descending order
    students.sort(key=lambda x: x[1], reverse=True)
    
    # Initialize the maximum sum and the current sum
    max_sum = 0
    current_sum = 0
    
    # Iterate through the sorted students
    for i in range(n):
        # Check if the current student can work with all previous students
        can_work = True
        for j in range(i):
            if (students[i][0] & students[j][0]) == students[i][0]:
                can_work = False
                break
        
        if can_work:
            # If the student can work, add their skill level to the current sum
            current_sum += students[i][1]
            # Update the maximum sum if necessary
            max_sum = max(max_sum, current_sum)
        else:
            # If the student can't work, reset the current sum
            current_sum = students[i][1]
    
    # Return the maximum sum, or 0 if no valid group was found
    return max_sum if max_sum > 0 else 0

# Read input
n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# Call the function and print the result
print(max_skill_sum(n, a, b))