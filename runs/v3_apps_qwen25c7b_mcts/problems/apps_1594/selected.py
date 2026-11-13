def find_song_at_time(n, m, playlist, queries):
    result = []
    current_time = 0
    song_index = 0
    
    for i in range(m):
        target_time = queries[i]
        
        while current_time < target_time:
            if song_index >= n:
                break
            song_count, song_duration = playlist[song_index]
            if current_time + song_count * song_duration >= target_time:
                result.append(song_index + 1)
                break
            current_time += song_count * song_duration
            song_index += 1
    
    return result

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

playlist = []
index = 2
for _ in range(n):
    count = int(data[index])
    duration = int(data[index + 1])
    playlist.append((count, duration))
    index += 2

queries = [int(data[index + i]) for i in range(m)]

# Output the result
result = find_song_at_time(n, m, playlist, queries)
print(*result)