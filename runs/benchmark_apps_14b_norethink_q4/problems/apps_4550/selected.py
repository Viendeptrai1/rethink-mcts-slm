import sys

def main():
    a, b, c = map(int, sys.stdin.readline().split())
    total_candies = a + b + c
    
    # Check if the total number of candies is even
    if total_candies % 2 != 0:
        print("No")
        return
    
    half_candies = total_candies // 2
    
    # Check if any combination of two packs equals half of the total candies
    if a + b == half_candies or a + c == half_candies or b + c == half_candies:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()