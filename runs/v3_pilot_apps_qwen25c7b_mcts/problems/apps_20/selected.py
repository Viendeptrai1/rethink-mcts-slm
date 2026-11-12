from sys import stdin, stdout

def is_palindrome(time_str):
    return time_str == time_str[::-1]

def time_to_minutes(time_str):
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

def minutes_to_time(minutes):
    h = minutes // 60
    m = minutes % 60
    return f"{h:02}:{m:02}"

def min_minutes_to_palindrome(current_time):
    current_minutes = time_to_minutes(current_time)
    for i in range(1440):  # 24 hours * 60 minutes
        next_time = minutes_to_time((current_minutes + i) % 1440)
        if is_palindrome(next_time):
            return i
    return 0

if __name__ == "__main__":
    current_time = stdin.read().strip()
    result = min_minutes_to_palindrome(current_time)
    stdout.write(str(result) + '\n')