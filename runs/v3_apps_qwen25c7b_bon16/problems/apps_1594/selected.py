import sys

def find_song(v, play_list):
    current_time = 0
    song_index = 0
    
    for i in range(len(play_list)):
        song_count, song_duration = play_list[i]
        if v <= current_time + song_count * song_duration:
            return i + 1
        else:
            current_time += song_count * song_duration
    
    return -1

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    play_list = []
    for _ in range(n):
        song_count = int(data[index])
        song_duration = int(data[index + 1])
        play_list.append((song_count, song_duration))
        index += 2
    
    queries = []
    for _ in range(m):
        queries.append(int(data[index]))
        index += 1
    
    results = [find_song(v, play_list) for v in queries]
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()