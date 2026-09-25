import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    a = int(data[0])
    b = int(data[1])
    c = int(data[2])
    
    # Calculate the maximum number of days the cat can eat
    max_days = 0
    
    # Try starting from each day of the week
    for start_day in range(7):
        days = 0
        fish_left = a
        rabbit_left = b
        chicken_left = c
        
        while True:
            if start_day % 7 == 0 or start_day % 7 == 3 or start_day % 7 == 6:
                if fish_left > 0:
                    fish_left -= 1
                else:
                    break
            elif start_day % 7 == 1 or start_day % 7 == 5:
                if rabbit_left > 0:
                    rabbit_left -= 1
                else:
                    break
            else:
                if chicken_left > 0:
                    chicken_left -= 1
                else:
                    break
            
            days += 1
            start_day += 1
        
        max_days = max(max_days, days)
    
    print(max_days)

if __name__ == "__main__":
    main()