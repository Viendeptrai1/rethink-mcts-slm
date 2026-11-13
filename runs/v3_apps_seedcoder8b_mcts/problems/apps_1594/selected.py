def find_song_playing_at_moments(n, m, playlist, moments):
    # Calculate the total duration of the playlist
    total_duration = 0
    song_end_times = []

    for c_i, t_i in playlist:
        total_duration += c_i * t_i
        song_end_times.append(total_duration)

    # Prepare the result list
    result = []

    # For each moment, find the song playing at that time
    for moment in moments:
        # Binary search to find the song playing at the moment
        low, high = 0, n - 1
        while low < high:
            mid = (low + high) // 2
            if song_end_times[mid] < moment:
                low = mid + 1
            else:
                high = mid

        # Determine the song number
        if song_end_times[low] >= moment:
            # Find the exact song by checking the previous song's end time
            if low == 0 or song_end_times[low - 1] < moment:
                result.append(low + 1)
            else:
                result.append(low)
        else:
            result.append(n)

    # Print the result
    for res in result:
        print(res)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

playlist = []
index = 2
for _ in range(n):
    c_i = int(data[index])
    t_i = int(data[index + 1])
    playlist.append((c_i, t_i))
    index += 2

moments = []
for _ in range(m):
    moments.append(int(data[index]))
    index += 1

# Call the function with the input data
find_song_playing_at_moments(n, m, playlist, moments)