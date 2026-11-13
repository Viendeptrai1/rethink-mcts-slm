def min_schools_to_make_up(n, m, k, powers, schools, chosen_ones):
    # Create a list of tuples (power, school, index)
    students = sorted(zip(powers, schools, range(1, n + 1)), reverse=True)
    
    # Dictionary to store the strongest student per school
    strongest_per_school = {}
    
    # Populate the dictionary with the strongest student per school
    for power, school, index in students:
        if school not in strongest_per_school or power > strongest_per_school[school][0]:
            strongest_per_school[school] = (power, index)
    
    # List to keep track of which schools need to be changed
    schools_to_change = []
    
    # Check which students are already among the chosen ones
    chosen_students = set(chosen_ones)
    
    # Iterate through the strongest students and check if they are chosen
    for power, school, index in students:
        if index in chosen_students:
            continue
        
        # If the student is not chosen, find the next strongest student in the same school
        if power == strongest_per_school[school][0]:
            continue
        
        # Find the next strongest student in the same school
        next_strongest_power, next_strongest_index = strongest_per_school[school]
        
        # If the next strongest student is also not chosen, add the school to the list
        if next_strongest_index not in chosen_students:
            schools_to_change.append(school)
            break
    
    return len(set(schools_to_change))

# Example usage
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

powers = list(map(int, data[3:3+n]))
schools = list(map(int, data[3+n:3+2*n]))
chosen_ones = list(map(int, data[3+2*n:]))

result = min_schools_to_make_up(n, m, k, powers, schools, chosen_ones)
print(result)