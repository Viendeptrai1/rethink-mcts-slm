import sys
import heapq

def min_schools_to_make_up(n, m, k, powers, schools, chosen_ones):
    # Create a list of tuples (power, index, school)
    students = [(powers[i], i, schools[i]) for i in range(n)]
    
    # Sort students by power in descending order
    students.sort(reverse=True)
    
    # Create a dictionary to store the strongest student in each school
    strongest_in_school = {}
    for power, index, school in students:
        if school not in strongest_in_school or power > strongest_in_school[school][0]:
            strongest_in_school[school] = (power, index)
    
    # Check which chosen ones are not the strongest in their schools
    not_strongest = set()
    for chosen_one in chosen_ones:
        if strongest_in_school[schools[chosen_one - 1]][1] != chosen_one - 1:
            not_strongest.add(chosen_one)
    
    # The number of schools to make up is the number of chosen ones that are not the strongest in their schools
    return len(not_strongest)

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

powers = list(map(int, data[3:3 + n]))
schools = list(map(int, data[3 + n:3 + 2 * n]))
chosen_ones = list(map(int, data[3 + 2 * n:3 + 2 * n + k]))

# Calculate and print the result
result = min_schools_to_make_up(n, m, k, powers, schools, chosen_ones)
print(result)