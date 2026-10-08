import sys
import heapq

def main():
    import sys
    import heapq

    def readints():
        return list(map(int, sys.stdin.readline().split()))

    n = readints()[0]
    fogs = []

    for _ in range(n):
        mi, di, li, ri, hi, dd, dx, dh = readints()
        fogs.append((mi, di, li, ri, hi, dd, dx, dh))

    def get_fog_rectangles(fog):
        mi, di, li, ri, hi, dd, dx, dh = fog
        rectangles = []
        for k in range(mi):
            day = di + k * dd
            l = li + k * dx
            r = ri + k * dx
            h = hi + k * dh
            rectangles.append((day, l, r, h))
        return rectangles

    all_rectangles = []
    for fog in fogs:
        all_rectangles.extend(get_fog_rectangles(fog))

    all_rectangles.sort()

    def is_covered(rect, covered_regions):
        l, r, h = rect
        for cl, cr, ch in covered_regions:
            if l >= cl and r <= cr and h <= ch:
                return True
        return False

    def merge_intervals(intervals):
        intervals.sort()
        merged = []
        current_start, current_end, current_height = intervals[0]

        for start, end, height in intervals[1:]:
            if start > current_end:
                merged.append((current_start, current_end, current_height))
                current_start, current_end, current_height = start, end, height
            else:
                current_end = max(current_end, end)
                current_height = max(current_height, height)

        merged.append((current_start, current_end, current_height))
        return merged

    def add_patch(covered_regions, new_patch):
        new_start, new_end, new_height = new_patch
        new_covered = []
        added = False

        for start, end, height in covered_regions:
            if new_end <= start:
                if not added:
                    new_covered.append((new_start, new_end, new_height))
                    added = True
                new_covered.append((start, end, height))
            elif new_start >= end:
                new_covered.append((start, end, height))
            else:
                overlap_start = max(new_start, start)
                overlap_end = min(new_end, end)
                overlap_height = max(new_height, height)
                new_covered.append((start, overlap_start, height))
                new_covered.append((overlap_start, overlap_end, overlap_height))
                new_covered.append((overlap_end, end, height))
                if new_start < start:
                    new_covered.append((new_start, start, new_height))
                if new_end > end:
                    new_covered.append((end, new_end, new_height))
                added = True

        if not added:
            new_covered.append((new_start, new_end, new_height))

        return merge_intervals(new_covered)

    covered_regions = []
    missed_count = 0

    for day, l, r, h in all_rectangles:
        if not is_covered((l, r, h), covered_regions):
            missed_count += 1
            covered_regions = add_patch(covered_regions, (l, r, h))

    print(missed_count)

if __name__ == "__main__":
    main()