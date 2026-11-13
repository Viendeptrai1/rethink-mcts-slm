import sys

def valid_time(time_str):
    h, m = map(int, time_str.split(':'))
    return 0 <= h <= 23 and 0 <= m <= 59

def generate_times(current_time):
    h, m = map(int, current_time.split(':'))
    times = set()
    
    def dfs(hh, mm, steps=0):
        if (hh, mm) not in times:
            times.add((hh, mm))
            if steps == 6:
                return
            for dh, dm in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nh, nm = (hh + dh) % 24, (mm + dm) % 60
                dfs(nh, nm, steps + 1)
    
    dfs(h, m)
    return times

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    original_time = data[0]
    current_time = data[1]
    
    times = generate_times(current_time)
    
    times_list = list(times)
    times_list.sort(key=lambda x: (x[0], x[1]))
    
    print(len(times_list))
    for time in times_list:
        print(f"{time[0]:02}:{time[1]:02}")

if __name__ == "__main__":
    main()