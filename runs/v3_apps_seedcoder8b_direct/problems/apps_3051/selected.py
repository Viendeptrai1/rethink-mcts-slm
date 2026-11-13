def count_missed_fogs(n, fogs):
    from sortedcontainers import SortedList

    # Helper function to check if a point is inside a rectangle
    def is_inside(x, y, rect):
        l, r, h = rect
        return l <= x <= r and 0 <= y <= h

    # Helper function to check if two rectangles overlap
    def do_overlap(rect1, rect2):
        l1, r1, h1 = rect1
        l2, r2, h2 = rect2
        return not (r1 < l2 or r2 < l1 or h1 < 0 or h2 < 0)

    # Helper function to merge two rectangles
    def merge_rectangles(rect1, rect2):
        l1, r1, h1 = rect1
        l2, r2, h2 = rect2
        return (min(l1, l2), max(r1, r2), max(h1, h2))

    # Initialize the list of active fogs and nets
    active_fogs = []
    nets = SortedList()

    # Process each fog
    for fog in fogs:
        m_i, d_i, l_i, r_i, h_i, delta_d_i, delta_x_i, delta_h_i = fog

        # Generate all fogs for this originator
        for k in range(m_i):
            x = l_i + k * delta_x_i
            y = h_i + k * delta_h_i
            day = d_i + k * delta_d_i
            active_fogs.append((day, x, y))

        # Sort fogs by day
        active_fogs.sort()

        # Process each day
        current_day = 0
        while active_fogs and active_fogs[0][0] <= current_day:
            day, x, y = active_fogs.pop(0)

            # If the current day is different, add new nets
            if day > current_day:
                # Find all missed fogs
                missed_fogs = 0
                for fog_day, fog_x, fog_y in active_fogs:
                    if fog_day > day:
                        break
                    if not any(is_inside(fog_x, fog_y, net) for net in nets):
                        missed_fogs += 1

                # Add new nets to cover missed fogs
                while missed_fogs > 0:
                    for fog_day, fog_x, fog_y in active_fogs:
                        if fog_day > day:
                            break
                        if not any(is_inside(fog_x, fog_y, net) for net in nets):
                            # Find the smallest net that can cover this fog
                            best_net = (fog_x, fog_x, fog_y)
                            for net in nets:
                                if do_overlap(net, (fog_x, fog_x, fog_y)):
                                    best_net = merge_rectangles(best_net, net)
                            nets.add(best_net)
                            missed_fogs -= 1
                            if missed_fogs == 0:
                                break

                current_day = day

    # Count total missed fogs
    total_missed_fogs = 0
    for fog_day, fog_x, fog_y in active_fogs:
        if not any(is_inside(fog_x, fog_y, net) for net in nets):
            total_missed_fogs += 1

    return total_missed_fogs

# Read input
n = int(input())
fogs = [tuple(map(int, input().split())) for _ in range(n)]

# Call the function and print the result
print(count_missed_fogs(n, fogs))