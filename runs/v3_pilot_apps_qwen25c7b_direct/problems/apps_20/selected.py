from sys import stdin, stdout

def is_palindrome(time_str):
    return time_str == time_str[::-1]

def min_minutes_to_palindrome(current_time):
    hours, minutes = map(int, current_time.split(':'))
    total_minutes = hours * 60 + minutes
    
    while True:
        if is_palindrome(f"{total_minutes // 60:02}:{total_minutes % 60:02}"):
            break
        total_minutes += 1
    
    return total_minutes - (hours * 60 + minutes)

if __name__ == "__main__":
    current_time = stdin.read().strip()
    result = min_minutes_to_palindrome(current_time)
    stdout.write(str(result) + '\n')