from sys import stdin, stdout

def find_lucky_time(x, hh, mm):
    target_minutes = hh * 60 + mm
    current_minute = target_minutes
    
    while True:
        current_hour = current_minute // 60 % 24
        current_minute %= 60
        
        if '7' in f"{current_hour:02d}{current_minute:02d}":
            return (target_minutes - current_minute) // x
        
        current_minute -= x

if __name__ == "__main__":
    x = int(stdin.readline().strip())
    hh, mm = map(int, stdin.readline().strip().split())
    
    result = find_lucky_time(x, hh, mm)
    stdout.write(str(result) + '\n')