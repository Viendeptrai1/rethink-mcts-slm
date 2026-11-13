def min_companies_to_assign(n, k, roads):
    # Initialize the number of companies to 1
    r = 1
    
    # Try assigning roads to 1 company and check if it meets the requirement
    while True:
        # Create a list to keep track of the count of roads per city
        city_roads_count = [0] * n
        
        # Assign roads to the current number of companies
        for i in range(len(roads)):
            city_roads_count[roads[i][0] - 1] += 1
            city_roads_count[roads[i][1] - 1] += 1
        
        # Count the number of cities that have two or more roads of the same company
        bad_cities = sum(1 for count in city_roads_count if count > 2)
        
        # If the number of bad cities is within the limit, return the number of companies and assignments
        if bad_cities <= k:
            return r, [i % r + 1 for i in range(len(roads))]
        
        # Otherwise, try with more companies
        r += 1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])

roads = []
for i in range(n-1):
    x_i = int(data[2 + 2*i]) - 1
    y_i = int(data[3 + 2*i]) - 1
    roads.append((x_i, y_i))

result_r, result_assignments = min_companies_to_assign(n, k, roads)

print(result_r)
print(" ".join(map(str, result_assignments)))