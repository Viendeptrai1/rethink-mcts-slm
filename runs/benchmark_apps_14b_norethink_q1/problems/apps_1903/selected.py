import sys
import bisect

def max_significance(n, m, d, physics_cups, informatics_cups):
    # Sort cups by significance in descending order
    physics_cups.sort(key=lambda x: -x[0])
    informatics_cups.sort(key=lambda x: -x[0])
    
    # Preprocess the cups to ensure that if a cup with significance x is taken,
    # all cups with significance greater than x must also be taken
    physics_prefix_sum = []
    current_width = 0
    current_significance = 0
    for c, w in physics_cups:
        if current_width + w <= d:
            current_width += w
            current_significance += c
        physics_prefix_sum.append((current_width, current_significance))
    
    informatics_prefix_sum = []
    current_width = 0
    current_significance = 0
    for c, w in informatics_cups:
        if current_width + w <= d:
            current_width += w
            current_significance += c
        informatics_prefix_sum.append((current_width, current_significance))
    
    # Binary search to find the maximum significance
    max_significance = 0
    
    for pw, ps in physics_prefix_sum:
        if pw > d:
            continue
        remaining_width = d - pw
        idx = bisect.bisect_right(informatics_prefix_sum, (remaining_width, float('inf')))
        if idx > 0:
            iw, isig = informatics_prefix_sum[idx - 1]
            max_significance = max(max_significance, ps + isig)
    
    for iw, isig in informatics_prefix_sum:
        if iw > d:
            continue
        remaining_width = d - iw
        idx = bisect.bisect_right(physics_prefix_sum, (remaining_width, float('inf')))
        if idx > 0:
            pw, ps = physics_prefix_sum[idx - 1]
            max_significance = max(max_significance, isig + ps)
    
    return max_significance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    d = int(data[index + 2])
    index += 3
    
    physics_cups = []
    for _ in range(n):
        c = int(data[index])
        w = int(data[index + 1])
        physics_cups.append((c, w))
        index += 2
    
    informatics_cups = []
    for _ in range(m):
        c = int(data[index])
        w = int(data[index + 1])
        informatics_cups.append((c, w))
        index += 2
    
    result = max_significance(n, m, d, physics_cups, informatics_cups)
    print(result)

if __name__ == "__main__":
    main()