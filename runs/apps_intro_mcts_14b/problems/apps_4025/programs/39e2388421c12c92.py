import sys

def max_days(a, b, c):
    # Calculate the maximum number of days the cat can eat without additional food purchases
    # by considering the optimal starting day of the week.
    
    # The cat eats fish food on Mondays, Thursdays, and Sundays (3 days per week)
    # The cat eats rabbit stew on Tuesdays and Saturdays (2 days per week)
    # The cat eats chicken stake on Wednesdays, Fridays, and sometimes Saturdays (2 days per week)
    
    # Calculate the maximum number of weeks the cat can survive with each type of food
    weeks_fish = a // 3
    weeks_rabbit = b // 2
    weeks_chicken = c // 2
    
    # Calculate the remaining days after full weeks
    remaining_fish = a % 3
    remaining_rabbit = b % 2
    remaining_chicken = c % 2
    
    # Calculate the total number of days the cat can survive
    total_days = min(weeks_fish * 3 + remaining_fish, weeks_rabbit * 2 + remaining_rabbit, weeks_chicken * 2 + remaining_chicken)
    
    return total_days

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    a = int(data[0])
    b = int(data[1])
    c = int(data[2])
    result = max_days(a, b, c)
    print(result)

if __name__ == "__main__":
    main()