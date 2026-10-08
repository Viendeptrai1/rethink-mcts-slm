import sys
from bisect import bisect_left

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    c = []
    t = []
    for i in range(n):
        c.append(int(data[2 + 2 * i]))
        t.append(int(data[3 + 2 * i]))
    
    moments = [int(data[2 + 2 * n + i]) for i in range(m)]
    
    # Calculate the cumulative durations
    cumulative_durations = []
    total_duration = 0
    for i in range(n):
        total_duration += c[i] * t[i]
        cumulative_durations.append(total_duration)
    
    # Find the song number for each moment
    results = []
    for moment in moments:
        index = bisect_left(cumulative_durations, moment)
        if index == 0:
            results.append(1)
        else:
            results.append(index + 1)
    
    # Print the results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()