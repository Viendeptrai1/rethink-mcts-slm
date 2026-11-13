def find_optimal_intersection(n, citizens, d):
    # Extract x and y coordinates
    x_coords = sorted(citizen[0] for citizen in citizens)
    y_coords = sorted(citizen[1] for citizen in citizens)

    # Function to calculate the total distance for a given intersection (x, y)
    def total_distance(x, y):
        return sum(abs(x - cx) + abs(y - cy) for cx, cy in citizens)

    # Function to check if a given intersection is valid
    def is_valid_intersection(x, y):
        return all(abs(x - cx) + abs(y - cy) <= d for cx, cy in citizens)

    # Binary search to find the optimal x-coordinate
    def find_optimal_x():
        low, high = 0, len(x_coords) - 1
        best_x, best_distance = x_coords[0], float('inf')

        while low <= high:
            mid = (low + high) // 2
            x = x_coords[mid]

            # Check if this x is a valid intersection
            if is_valid_intersection(x, y_coords[0]):
                dist = total_distance(x, y_coords[0])
                if dist < best_distance:
                    best_distance = dist
                    best_x = x

            # Move to the side with smaller total distance
            if mid > 0 and is_valid_intersection(x_coords[mid - 1], y_coords[0]):
                dist_left = total_distance(x_coords[mid - 1], y_coords[0])
                if dist_left < best_distance:
                    best_distance = dist_left
                    best_x = x_coords[mid - 1]

            if mid < len(x_coords) - 1 and is_valid_intersection(x_coords[mid + 1], y_coords[0]):
                dist_right = total_distance(x_coords[mid + 1], y_coords[0])
                if dist_right < best_distance:
                    best_distance = dist_right
                    best_x = x_coords[mid + 1]

            # Adjust search range
            if x - x_coords[0] > x_coords[-1] - x:
                high = mid - 1
            else:
                low = mid + 1

        return best_x, best_distance

    # Find the optimal x-coordinate
    optimal_x, optimal_distance = find_optimal_x()

    # Check if there's a valid y-coordinate
    for y in y_coords:
        if is_valid_intersection(optimal_x, y):
            return total_distance(optimal_x, y)

    return "impossible"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
citizens = [(int(data[i]), int(data[i + 1])) for i in range(1, 2 * n + 1, 2)]
d = int(data[2 * n + 1])

# Find and print the result
result = find_optimal_intersection(n, citizens, d)
print(result)