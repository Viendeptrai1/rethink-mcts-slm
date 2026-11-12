from datetime import datetime, timedelta

def min_minutes_to_palindrome(current_time):
    # Convert the input string to a datetime object
    current_hour, current_minute = map(int, current_time.split(':'))
    current_datetime = datetime.strptime(f"{current_hour:02}:{current_minute:02}", "%H:%M")
    
    # Function to check if a time is a palindrome
    def is_palindrome(time_str):
        return time_str == time_str[::-1]
    
    # Start checking from the next minute
    while True:
        # Format the current time as a string
        formatted_time = current_datetime.strftime("%H:%M")
        
        # Check if the current time is a palindrome
        if is_palindrome(formatted_time):
            break
        
        # Move to the next minute
        current_datetime += timedelta(minutes=1)
    
    # Calculate the difference in minutes
    minutes_to_sleep = (current_datetime - datetime.strptime(f"{current_hour:02}:{current_minute:02}", "%H:%M")).seconds // 60
    
    return minutes_to_sleep

# Example usage
if __name__ == "__main__":
    import sys
    input_time = sys.stdin.read().strip()
    result = min_minutes_to_palindrome(input_time)
    print(result)