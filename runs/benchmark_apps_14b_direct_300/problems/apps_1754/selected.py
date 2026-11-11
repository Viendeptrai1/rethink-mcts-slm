import sys

def min_schools_to_make_up(n, m, k, powers, schools, chosen_ones):
    # Create a dictionary to store the strongest student in each school
    strongest_in_school = {}
    for i in range(n):
        if schools[i] not in strongest_in_school or powers[i] > powers[strongest_in_school[schools[i]] - 1]:
            strongest_in_school[schools[i]] = i + 1
    
    # Check which chosen ones are already the strongest in their schools
    already_strongest = set()
    for chosen_one in chosen_ones:
        if strongest_in_school[schools[chosen_one - 1]] == chosen_one:
            already_strongest.add(chosen_one)
    
    # The number of chosen ones that are not already the strongest
    needed = k - len(already_strongest)
    
    # The minimum number of schools to make up is equal to the number of chosen ones that are not already the strongest
    return needed

# Read input
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