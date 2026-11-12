from sys import stdin, stdout

def is_palindrome(time_str):
    return time_str == time_str[::-1]

def min_minutes_to_palindrome(current_time):
    hours, minutes = map(int, current_time.split(':'))
    
    # Check if the current time is already a palindrome
    if is_palindrome(current_time):
        return 0
    
    # Calculate the next possible palindrome time
    while True:
        minutes += 1
        if minutes >= 60:
            minutes = 0
            hours += 1
            if hours >= 24:
                hours = 0
        
        next_time = f"{hours:02}:{minutes:02}"
        if is_palindrome(next_time):
            break
    
    # Calculate the difference in minutes
    current_minutes = int(current_time[:2]) * 60 + int(current_time[3:])
    next_minutes = int(next_time[:2]) * 60 + int(next_time[3:])
    return (next_minutes - current_minutes) % (24 * 60)

if __name__ == "__main__":
    current_time = stdin.readline().strip()
    result = min_minutes_to_palindrome(current_time)
    stdout.write(f"{result}\n")