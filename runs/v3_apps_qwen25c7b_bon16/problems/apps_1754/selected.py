def min_schools_to_make_up(n, m, k, powers, schools, chosens):
    # Create a list to store the strongest student per school
    strongest_per_school = [None] * (m + 1)
    
    # Find the strongest student in each school
    for i in range(n):
        if strongest_per_school[schools[i]] is None or powers[i] > powers[strongest_per_school[schools[i]]]:
            strongest_per_school[schools[i]] = i
    
    # Count how many of the Chosen Ones are already the strongest in their schools
    already_chosen = sum(1 for chosen in chosens if strongest_per_school[schools[chosen - 1]] == chosen - 1)
    
    # Calculate the number of additional schools needed
    additional_schools_needed = max(0, k - already_chosen)
    
    return additional_schools_needed

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

powers = list(map(int, data[3:3+n]))
schools = list(map(int, data[3+n:3+2*n]))
chosens = list(map(int, data[3+2*n:]))

print(min_schools_to_make_up(n, m, k, powers, schools, chosens))