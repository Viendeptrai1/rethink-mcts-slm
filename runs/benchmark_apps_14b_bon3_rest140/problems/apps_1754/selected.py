def min_schools_to_make_up(n, m, k, powers, schools, chosen_ones):
    # Create a dictionary to store the strongest student in each school
    strongest_in_school = {}
    for i in range(n):
        if schools[i] not in strongest_in_school or powers[i] > powers[strongest_in_school[schools[i]] - 1]:
            strongest_in_school[schools[i]] = i + 1
    
    # Create a set of schools where the chosen ones are the strongest
    chosen_schools = set()
    for chosen_one in chosen_ones:
        if strongest_in_school[schools[chosen_one - 1]] == chosen_one:
            chosen_schools.add(schools[chosen_one - 1])
    
    # The number of schools to make up is the total number of chosen ones minus the number of chosen schools
    return k - len(chosen_schools)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

powers = list(map(int, data[3:3+n]))
schools = list(map(int, data[3+n:3+2*n]))
chosen_ones = list(map(int, data[3+2*n:3+2*n+k]))

# Output the result
print(min_schools_to_make_up(n, m, k, powers, schools, chosen_ones))