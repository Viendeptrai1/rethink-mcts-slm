def find_song_playing_at_moments():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    index = 2
    play_list = []
    
    for _ in range(n):
        c_i = int(data[index])
        t_i = int(data[index + 1])
        play_list.append((c_i, t_i))
        index += 2
    
    moments = list(map(int, data[index:index + m]))
    
    # Calculate the total duration of the play list
    total_duration = sum(c_i * t_i for c_i, t_i in play_list)
    
    # Calculate the cumulative durations
    cumulative_durations = []
    current_duration = 0
    
    for c_i, t_i in play_list:
        current_duration += c_i * t_i
        cumulative_durations.append(current_duration)
    
    # Find the song playing at each moment
    results = []
    
    for moment in moments:
        # Binary search to find the song playing at the given moment
        low, high = 0, n - 1
        while low < high:
            mid = (low + high) // 2
            if cumulative_durations[mid] < moment:
                low = mid + 1
            else:
                high = mid
        
        # Determine the specific song within the segment
        segment_duration = cumulative_durations[low]
        if low > 0:
            segment_start_duration = cumulative_durations[low - 1]
        else:
            segment_start_duration = 0
        
        # Calculate the position within the current segment
        position_in_segment = moment - segment_start_duration
        
        # Determine the song number
        c_i, t_i = play_list[low]
        song_number = low + 1
        
        results.append(song_number)
    
    # Print the results
    for result in results:
        print(result)