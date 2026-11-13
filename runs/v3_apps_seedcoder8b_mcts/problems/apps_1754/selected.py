def min_schools_to_make_up(n, m, k, powers, schools, chosen_ones):
    from collections import defaultdict

    # Create a dictionary to store the strongest student in each school
    school_strongest = defaultdict(lambda: (0, 0))  # (power, student_id)

    # Fill the dictionary with the strongest student from each school
    for student_id in range(1, n + 1):
        power = powers[student_id - 1]
        school = schools[student_id - 1]
        if power > school_strongest[school][0]:
            school_strongest[school] = (power, student_id)

    # Create a set of the current schools of the chosen ones
    chosen_schools = set(schools[student_id - 1] for student_id in chosen_ones)

    # Count how many chosen ones are already in the strongest student of their school
    already_strongest = sum(1 for student_id in chosen_ones if school_strongest[schools[student_id - 1]][1] == student_id)

    # Calculate the number of additional schools needed
    additional_schools_needed = k - already_strongest

    return additional_schools_needed

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])
powers = list(map(int, data[3:n + 3]))
schools = list(map(int, data[n + 3:2 * n + 3]))
chosen_ones = list(map(int, data[2 * n + 3:2 * n + 3 + k]))

# Calculate and print the result
result = min_schools_to_make_up(n, m, k, powers, schools, chosen_ones)
print(result)