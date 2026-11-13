def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    song_info = []
    for _ in range(n):
        c_i = int(data[index])
        t_i = int(data[index + 1])
        index += 2
        song_info.append((c_i, t_i))
    
    moments = [int(data[index + i]) for i in range(m)]
    
    # Calculate the cumulative duration up to each song
    cumulative_durations = []
    total_duration = 0
    for c_i, t_i in song_info:
        total_duration += c_i * t_i
        cumulative_durations.append(total_duration)
    
    results = []
    for moment in moments:
        # Binary search to find which song is playing at the given moment
        low, high = 0, n - 1
        while low < high:
            mid = (low + high) // 2
            if cumulative_durations[mid] < moment:
                low = mid + 1
            else:
                high = mid
        
        # Find the exact song play moment
        current_duration = cumulative_durations[low] - (cumulative_durations[low - 1] if low > 0 else 0)
        song_c_i, song_t_i = song_info[low]
        
        # Calculate the position within the current song
        position_in_song = moment - (cumulative_durations[low - 1] if low > 0 else 0)
        # Find which instance of the song is playing at this moment
        instance_number = (position_in_song - 1) // song_t_i + 1
        
        results.append(low + 1)  # Songs are 1-indexed
    
    sys.stdout.write("\n".join(map(str, results)) + "\n")

if __name__ == "__main__":
    main()