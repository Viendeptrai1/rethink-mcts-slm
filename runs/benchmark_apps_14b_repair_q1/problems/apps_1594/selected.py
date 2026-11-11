def find_song_at_moment(n, m, playlist, moments):
    # Calculate cumulative durations
    cumulative_durations = []
    current_duration = 0
    for c, t in playlist:
        current_duration += c * t
        cumulative_durations.append(current_duration)
    
    # Function to find the song at a given moment using binary search
    def find_song(moment):
        low, high = 0, n - 1
        while low < high:
            mid = (low + high) // 2
            if cumulative_durations[mid] < moment:
                low = mid + 1
            else:
                high = mid
        return low + 1  # Convert zero-based index to one-based song number
    
    # Find the song for each moment
    result = [find_song(v) for v in moments]
    return result

# Read input
n, m = map(int, input().split())
playlist = [tuple(map(int, input().split())) for _ in range(n)]
moments = list(map(int, input().split()))

# Get the result
result = find_song_at_moment(n, m, playlist, moments)

# Print the result
for song_number in result:
    print(song_number)