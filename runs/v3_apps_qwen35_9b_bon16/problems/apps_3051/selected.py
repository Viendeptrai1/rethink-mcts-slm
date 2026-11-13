import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    # Parse originator fogs
    originators = []
    for _ in range(n):
        m = int(next(iterator))
        d = int(next(iterator))
        l = int(next(iterator))
        r = int(next(iterator))
        h = int(next(iterator))
        dd = int(next(iterator))
        dx = int(next(iterator))
        dh = int(next(iterator))
        originators.append({
            'm': m, 'd': d, 'l': l, 'r': r, 'h': h,
            'dd': dd, 'dx': dx, 'dh': dh
        })

    # Generate all fog events: (day, l, r, h)
    # Since we need to simulate day by day, and days can be large but sparse,
    # we will collect all unique days and process them in order.
    events = []
    for i in range(n):
        o = originators[i]
        for k in range(o['m']):
            day = o['d'] + k * o['dd']
            l = o['l'] + k * o['dx']
            r = o['r'] + k * o['dx']
            h = o['h'] + k * o['dh']
            # Store as a tuple (day, l, r, h)
            events.append((day, l, r, h))

    if not events:
        print(0)
        return

    events.sort(key=lambda x: x[0])

    # Group events by day
    days_map = {}
    for ev in events:
        day, l, r, h = ev
        if day not in days_map:
            days_map[day] = []
        days_map[day].append((l, r, h))

    sorted_days = sorted(days_map.keys())

    missed_count = 0
    # Current net coverage: we maintain a list of disjoint rectangles covering the net.
    # However, the net grows incrementally. On each day, we first identify all fogs present.
    # Then we calculate the minimum area to add to the existing net to cover all these fogs.
    # The existing net is the union of all patches added so far.
    # We need to represent the current net as a set of disjoint rectangles to efficiently check coverage and add new areas.
    
    # Representation of the net: list of disjoint rectangles (lx, rx, by, ty) sorted by x then y.
    # Actually, since we add rectangles arbitrarily, maintaining a canonical disjoint representation is key.
    # Given constraints (N=1000, M=100), total fogs = 100,000. Days could be up to 10^8 but only those with fogs matter.
    # Max distinct days is 100,000.
    # For each day, we have a list of fog rectangles. We need to cover them with the minimum addition to the current net.
    # This is equivalent to: New Net = Current Net U (Union of current day's fogs).
    # Cost = Area(New Net) - Area(Current Net).
    # Since we only care about the count of missed fogs (which is just the count of fogs not fully inside the current net),
    # we don't actually need to compute the area or the exact geometry of the net for the answer.
    # Wait, the problem asks for "total number of fogs that are missed".
    # "Missed" means the fog rectangle was NOT completely contained in the region covered by nets.
    # So for each day, for each fog present, we check if it is a subset of the current net coverage.
    # If not, it is missed.
    # The net coverage updates every day to include all fogs of that day (plus previous ones).
    # So we need to maintain the union of rectangles representing the net.
    
    # Algorithm:
    # 1. Maintain `net_rects`: a list of disjoint rectangles representing the current net coverage.
    #    Initially empty.
    # 2. For each day in sorted_days:
    #    a. Get list of fog rectangles for this day.
    #    b. For each fog rect, check if it is fully covered by `net_rects`.
    #       If not, increment missed_count.
    #    c. Add all fog rectangles (from this day) to `net_rects` (merge them with existing).
    #       Actually, the problem says: "workers add rectangular net patches ... so that the resulting array of nets would have caught all the fogs that day."
    #       This implies the net becomes the union of previous net and all fogs of that day.
    #       So step c is: Update `net_rects` = Union(`net_rects`, all fogs of today).
    
    # Helper to merge two sets of rectangles (list of rects) into one canonical disjoint list.
    # Function to merge a list of rects into a canonical disjoint list.
    def get_disjoint_union(rects):
        if not rects:
            return []
        # Sort by x, then by y
        sorted_rects = sorted(rects, key=lambda r: (r[0], r[1]))
        merged = []
        curr = sorted_rects[0]
        for next_r in sorted_rects[1:]:
            cx, crx, cby, ct_y = curr
            nx, nrx, nby, nt_y = next_r
            
            # Check overlap in x
            if nx >= crx:
                # Disjoint or touching in x (touching doesn't merge for area/coverage usually, but for union of regions, touching edges merge into one region if we consider closed intervals? 
                # Problem says "completely contained". If fog is [0, 1] and net is [0, 1], it's covered.
                # If net is [0, 1] and we add [1, 2], union is [0, 2].
                # So we treat intervals as closed.
                if nby <= ct_y:
                    # Merge: extend x to max(r), extend y to max(ty)
                    curr = (min(cx, nx), max(crx, nrx), min(cby, nby), max(ct_y, nt_y))
                else:
                    # X overlaps but Y doesn't overlap enough to merge into one rect?
                    # Wait, if X intervals overlap (nx < crx) but Y intervals are disjoint, they are two separate rectangles.
                    # My sort key is (x, y). If X overlaps, nx < crx.
                    # If they don't overlap in X (nx >= crx), they are separate unless we consider the previous logic.
                    # Let's refine the merge logic.
                    pass
            
            # Standard plane sweep for union of rectangles
            # Since we just need a canonical representation for the "next day" check, 
            # and the number of rects is small (up to 100 per day), we can use a simple O(K^2) or O(K log K) merge.
            
            # Let's re-implement a robust merge:
            # Collect all x-coords, sort, create vertical strips. In each strip, merge y-intervals.
            # This is more robust.
            pass
        
        # Let's use the strip method inside the function
        return merge_rects_by_strips(rects)

    def merge_rects_by_strips(rects):
        if not rects:
            return []
        
        # Collect all x coordinates
        xs = set()
        for r in rects:
            xs.add(r[0])
            xs.add(r[1])
        sorted_xs = sorted(list(xs))
        
        merged_rects = []
        
        for i in range(len(sorted_xs) - 1):
            x_start = sorted_xs[i]
            x_end = sorted_xs[i+1]
            # If x_start == x_end, skip (width 0)
            if x_start >= x_end:
                continue
                
            # Find all rects that cover this x-strip [x_start, x_end]
            active_y_intervals = []
            for r in rects:
                lx, rx, by, ty = r
                if lx <= x_start and rx >= x_end:
                    active_y_intervals.append((by, ty))
            
            if not active_y_intervals:
                continue
            
            # Merge y-intervals
            active_y_intervals.sort()
            merged_y = []
            curr_y = active_y_intervals[0]
            for next_y in active_y_intervals[1:]:
                if curr_y[0] <= next_y[0]: # Overlap or touch
                    curr_y = (min(curr_y[0], next_y[0]), max(curr_y[1], next_y[1]))
                else:
                    merged_y.append(curr_y)
                    curr_y = next_y
            merged_y.append(curr_y)
            
            for (by, ty) in merged_y:
                merged_rects.append((x_start, x_end, by, ty))
        
        return merged_rects

    # Initial net is empty
    current_net = []

    # Helper to check if a fog rect is covered by current_net
    def is_fog_covered(fog_l, fog_r, fog_h, net_rects):
        # Fog is [fog_l, fog_r] x [0, fog_h]
        # We need to check if every point in fog is in net.
        # This is equivalent to: Is the union of intersections of fog and net_rects equal to fog?
        # Or simpler: For every unit (or strip) in fog, is it covered?
        # Given small N, we can iterate over the canonical strips of the fog itself?
        # Better: Check if the fog is a subset of the union of net_rects.
        # Since net_rects is a list of disjoint rects, we can check if the area of fog covered by net equals area of fog.
        # Area of fog = (fog_r - fog_l) * fog_h
        # Covered area = sum of areas of (fog intersect net_rect)
        # Intersection of two rects [l1, r1]x[h1] and [l2, r2]x[0, h2] is [max(l1, l2), min(r1, r2)] x [0, min(h1, h2)] (since net starts at 0)
        # Note: Fog height is from 0 to h. Net rects are arbitrary.
        # Intersection logic:
        # x_overlap: max(l_f, l_n) to min(r_f, r_n)
        # y_overlap: 0 to min(h_f, t_n) (since fog bottom is 0, net bottom is 0? No, net rects can start > 0)
        # Actually fog is [0, h_f]. Net rect is [0, ty]. Intersection in y is [0, min(h_f, ty)].
        # Wait, net rects are [by, ty]. Fog is [0, h_f].
        # Intersection in y: [max(0, by), min(h_f, ty)].
        # If max > min, no overlap in Y.
        
        total_covered_area = 0
        fog_area = (fog_r - fog_l) * fog_h
        
        for (nlx, nrx, nby, nty) in net_rects:
            # Intersection X
            ix1 = max(fog_l, nlx)
            ix2 = min(fog_r, nrx)
            if ix1 >= ix2:
                continue
            
            # Intersection Y
            iy1 = max(0, nby)
            iy2 = min(fog_h, nty)
            if iy1 >= iy2:
                continue
            
            total_covered_area += (ix2 - ix1) * (iy2 - iy1)
        
        return total_covered_area == fog_area

    for day in sorted_days:
        fogs = days_map[day]
        missed = 0
        for (fl, fr, fh) in fogs:
            if not is_fog_covered(fl, fr, fh, current_net):
                missed += 1
        missed_count += missed
        
        # Update net: Union of current_net and all fogs of this day
        all_fogs_rects = []
        for (fl, fr, fh) in fogs:
            # Fog rect: [fl, fr] x [0, fh]
            all_fogs_rects.append((fl, fr, 0, fh))
        
        new_fogs_union = merge_rects_by_strips(all_fogs_rects)
        # Merge current_net and new_fogs_union
        current_net = merge_rects_by_strips(current_net + new_fogs_union)

    print(missed_count)

if __name__ == '__main__':
    solve()