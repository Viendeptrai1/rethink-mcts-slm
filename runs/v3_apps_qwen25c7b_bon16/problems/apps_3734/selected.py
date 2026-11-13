import sys

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def is_possible(day1, day2):
    index1 = days.index(day1)
    index2 = days.index(day2)
    return (index1 + 30) % 7 == index2 or (index1 + 31) % 7 == index2

def main():
    day1 = sys.stdin.readline().strip()
    day2 = sys.stdin.readline().strip()
    if is_possible(day1, day2):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()