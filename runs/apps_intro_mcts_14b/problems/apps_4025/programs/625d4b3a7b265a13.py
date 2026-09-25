import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    a = int(data[0])
    b = int(data[1])
    c = int(data[2])
    
    # Calculate the maximum number of days for each starting day
    max_days = min(a // 3 + b // 2 + c, 
                   a // 3 + b // 2 + c + (a % 3 > 0), 
                   a // 3 + b // 2 + c + (b % 2 > 0), 
                   a // 3 + b // 2 + c + (a % 3 > 0) + (b % 2 > 0), 
                   a // 3 + b // 2 + c + (c > 0), 
                   a // 3 + b // 2 + c + (a % 3 > 0) + (c > 0), 
                   a // 3 + b // 2 + c + (b % 2 > 0) + (c > 0), 
                   a // 3 + b // 2 + c + (a % 3 > 0) + (b % 2 > 0) + (c > 0))
    
    print(max_days)

if __name__ == "__main__":
    main()