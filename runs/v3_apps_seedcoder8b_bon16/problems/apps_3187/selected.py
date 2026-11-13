def min_total_distance(n, citizens, d):
    from itertools import product

    x_coords = sorted(set(x for x, y in citizens))
    y_coords = sorted(set(y for x, y in citizens))

    min_total_distance = float('inf')
    found = False

    # Consider all possible intersections that are within the max distance `d`
    for x_star in x_coords:
        for y_star in y_coords:
            total_distance = 0
            for x, y in citizens:
                dist = abs(x - x_star) + abs(y - y_star)
                if dist > d:
                    break
                total_distance += dist
            else:
                found = True
                if total_distance < min_total_distance:
                    min_total_distance = total_distance

    if found:
        return min_total_distance
    else:
        return "impossible"

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()

    n = int(data[0])
    citizens = []
    index = 1
    for _ in range(n):
        x = int(data[index])
        y = int(data[index + 1])
        citizens.append((x, y))
        index += 2

    d = int(data[index])

    result = min_total_distance(n, citizens, d)
    print(result)

if __name__ == "__main__":
    main()