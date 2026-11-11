import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    index = 2
    playlist = []
    for _ in range(n):
        c_i = int(data[index])
        t_i = int(data[index + 1])
        playlist.append((c_i, t_i))
        index += 2
    
    moments = list(map(int, data[index:index + m]))
    
    current_time = 0
    song_index = 0
    result = []
    
    for moment in moments:
        while current_time + playlist[song_index][0] * playlist[song_index][1] < moment:
            current_time += playlist[song_index][0] * playlist[song_index][1]
            song_index += 1
        
        remaining_time = moment - current_time
        song_number = song_index + 1
        result.append(song_number)
    
    for res in result:
        print(res)

if __name__ == "__main__":
    main()