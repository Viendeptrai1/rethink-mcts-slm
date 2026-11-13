def min_cost_to_white(n, m, rectangles):
    events = []
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 0, y1, y2))
        events.append((x2 + 1, 1, y1, y2))
    events.sort()

    total_cost = 0
    active = []
    last_x = 0

    for x, event_type, y1, y2 in events:
        if x > last_x:
            if active:
                max_y = max(y for y, _ in active)
                min_y = min(y for y, _ in active)
                total_cost += x - last_x
            last_x = x

        if event_type == 0:  # Start of rectangle
            active.append((y1, 1))
            active.append((y2 + 1, -1))
        else:  # End of rectangle
            active.append((y1, -1))
            active.append((y2 + 1, 1))

        active.sort()
        count = 0
        for y, change in active:
            count += change
            if count == 0:
                active.remove((y, change))

    return total_cost

if __name__ == "__main__":
    n, m = map(int, input().split())
    rectangles = [list(map(int, input().split())) for _ in range(m)]
    print(min_cost_to_white(n, m, rectangles))