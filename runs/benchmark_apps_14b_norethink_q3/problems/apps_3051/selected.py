import sys
from heapq import heappush, heappop

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    index += 1
    
    events = []
    for _ in range(n):
        mi = int(data[index])
        di = int(data[index + 1])
        li = int(data[index + 2])
        ri = int(data[index + 3])
        hi = int(data[index + 4])
        delta_di = int(data[index + 5])
        delta_xi = int(data[index + 6])
        delta_hi = int(data[index + 7])
        index += 8
        
        for k in range(mi):
            day = di + k * delta_di
            l = li + k * delta_xi
            r = ri + k * delta_xi
            h = hi + k * delta_hi
            heappush(events, (day, l, r, h))
    
    active_fogs = []
    missed_fogs = 0
    current_day = 0
    current_coverage = []
    
    while events:
        day, l, r, h = heappop(events)
        
        # Remove fogs that have disappeared
        while active_fogs and active_fogs[0][0] < day:
            _, start, end, height = heappop(active_fogs)
            if not current_coverage:
                missed_fogs += 1
            else:
                missed_fogs += count_missed(current_coverage, start, end, height)
        
        # Add the new fog to active fogs
        heappush(active_fogs, (day + delta_di, l, r, h))
        
        # Update current coverage
        current_coverage = update_coverage(current_coverage, l, r, h)
    
    # Check for any remaining fogs
    while active_fogs:
        _, start, end, height = heappop(active_fogs)
        if not current_coverage:
            missed_fogs += 1
        else:
            missed_fogs += count_missed(current_coverage, start, end, height)
    
    print(missed_fogs)

def count_missed(coverage, start, end, height):
    missed = 0
    i = 0
    while i < len(coverage):
        c_start, c_end, c_height = coverage[i]
        if c_end <= start:
            i += 1
        elif c_start >= end:
            break
        else:
            overlap_start = max(start, c_start)
            overlap_end = min(end, c_end)
            overlap_height = min(height, c_height)
            missed += (overlap_end - overlap_start) * (height - overlap_height)
            if c_end > end:
                coverage[i] = (end, c_end, c_height)
                break
            else:
                del coverage[i]
    return missed

def update_coverage(coverage, start, end, height):
    new_coverage = []
    i = 0
    while i < len(coverage):
        c_start, c_end, c_height = coverage[i]
        if c_end <= start:
            new_coverage.append((c_start, c_end, c_height))
            i += 1
        elif c_start >= end:
            break
        else:
            overlap_start = max(start, c_start)
            overlap_end = min(end, c_end)
            overlap_height = max(height, c_height)
            if c_start < overlap_start:
                new_coverage.append((c_start, overlap_start, c_height))
            new_coverage.append((overlap_start, overlap_end, overlap_height))
            if c_end > overlap_end:
                new_coverage.append((overlap_end, c_end, c_height))
                break
            else:
                del coverage[i]
    new_coverage.extend(coverage[i:])
    return new_coverage

if __name__ == "__main__":
    main()