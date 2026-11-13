def min_schools_to_make_up(n, m, k, powers, schools, chosen_ones):
    # Find out the current max power in each school
    school_max_power = {}
    for student_id in range(n):
        school = schools[student_id]
        power = powers[student_id]
        if school in school_max_power:
            school_max_power[school] = max(school_max_power[school], power)
        else:
            school_max_power[school] = power

    # Check how many chosen ones are currently not in the strongest spot of their school
    not_strongest_chosen_ones = 0
    for chosen_one in chosen_ones:
        student_id = chosen_one - 1
        school = schools[student_id]
        if powers[student_id] < school_max_power[school]:
            not_strongest_chosen_ones += 1

    # The minimum number of new schools to be made up is the number of Chosen Ones not in the strongest position
    return not_strongest_chosen_ones

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])
powers = list(map(int, data[3:n+3]))
schools = list(map(int, data[n+3:2*n+3]))
chosen_ones = list(map(int, data[2*n+3:2*n+3+k]))

# Call the function and print the result
result = min_schools_to_make_up(n, m, k, powers, schools, chosen_ones)
print(result)