import heapq
from collections import defaultdict

def min_schools_to_make_up(n, m, k, powers, schools, chosen_ones):
    # Create a dictionary to store the strongest student in each school
    strongest_per_school = {}
    
    # Priority queue to keep track of the strongest students
    pq = []
    
    # Populate the priority queue and the dictionary
    for i in range(n):
        heapq.heappush(pq, (-powers[i], schools[i]))
        if schools[i] not in strongest_per_school or powers[i] > strongest_per_school[schools[i]]:
            strongest_per_school[schools[i]] = powers[i]
    
    # Set to keep track of schools that need replacement
    schools_to_replace = set()
    
    # Iterate over the chosen ones and check if they can be replaced
    for co in chosen_ones:
        current_school = schools[co - 1]
        if powers[co - 1] != strongest_per_school[current_school]:
            schools_to_replace.add(current_school)
    
    # Return the number of unique schools that need replacement
    return len(schools_to_replace)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    
    powers = list(map(int, data[3:3+n]))
    schools = list(map(int, data[3+n:3+2*n]))
    chosen_ones = list(map(int, data[3+2*n:3+2*n+k]))
    
    result = min_schools_to_make_up(n, m, k, powers, schools, chosen_ones)
    print(result)