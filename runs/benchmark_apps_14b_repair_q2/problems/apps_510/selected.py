def min_performance_duration(a, b, c, d):
    # Sort the initial positions
    positions = sorted([a, b, c])
    
    # Calculate the required gaps
    gap1 = max(0, d - (positions[1] - positions[0]))
    gap2 = max(0, d - (positions[2] - positions[1]))
    
    # The total time is the sum of the required gaps
    return gap1 + gap2

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    a = int(data[0])
    b = int(data[1])
    c = int(data[2])
    d = int(data[3])
    result = min_performance_duration(a, b, c, d)
    print(result)

if __name__ == "__main__":
    main()