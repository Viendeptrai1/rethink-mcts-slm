import sys

def main():
    import sys
    import sys
    import sys
    
    n = int(sys.stdin.readline().strip())
    segments = []
    
    for _ in range(n):
        l, r = map(int, sys.stdin.readline().strip().split())
        segments.append((l, r))
    
    # Sort segments by their starting points
    segments.sort()
    
    # Calculate the intersection of all segments
    left = segments[0][0]
    right = segments[0][1]
    for i in range(1, n):
        left = max(left, segments[i][0])
        right = min(right, segments[i][1])
    
    # Calculate the maximum intersection length after removing one segment
    max_length = 0
    for i in range(n):
        if i == 0:
            current_left = segments[1][0]
            current_right = segments[1][1]
            for j in range(2, n):
                current_left = max(current_left, segments[j][0])
                current_right = min(current_right, segments[j][1])
        elif i == n - 1:
            current_left = segments[0][0]
            current_right = segments[0][1]
            for j in range(1, n - 1):
                current_left = max(current_left, segments[j][0])
                current_right = min(current_right, segments[j][1])
        else:
            current_left = segments[0][0]
            current_right = segments[0][1]
            for j in range(1, i):
                current_left = max(current_left, segments[j][0])
                current_right = min(current_right, segments[j][1])
            for j in range(i + 1, n):
                current_left = max(current_left, segments[j][0])
                current_right = min(current_right, segments[j][1])
        
        max_length = max(max_length, max(0, current_right - current_left))
    
    print(max_length)

if __name__ == "__main__":
    main()