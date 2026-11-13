def find_song_at_time(n, m, playlist, queries):
    # Calculate the cumulative durations of each song
    cumulative_durations = [0] * (n + 1)
    current_duration = 0
    for i in range(n):
        cumulative_durations[i + 1] = current_duration + playlist[i][0] * playlist[i][1]
        current_duration = cumulative_durations[i + 1]

    # Find the song playing at each query time
    results = []
    for query in queries:
        # Binary search to find the song
        left, right = 0, n
        while left < right:
            mid = (left + right) // 2
            if cumulative_durations[mid] <= query:
                left = mid + 1
            else:
                right = mid
        results.append(left)

    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

playlist = []
for i in range(n):
    c_i = int(data[2 + 2 * i])
    t_i = int(data[3 + 2 * i])
    playlist.append((c_i, t_i))

queries = list(map(int, data[2 + 2 * n:]))

# Get the result
result = find_song_at_time(n, m, playlist, queries)

# Print the result
print(" ".join(map(str, result)))