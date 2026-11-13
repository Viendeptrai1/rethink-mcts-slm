import sys

def count_missed_trains(s):
    s = int(s, 2)
    count = 0
    k = 0
    while 4**k < s:
        count += 1
        k += 1
    return count

if __name__ == "__main__":
    s = sys.stdin.readline().strip()
    print(count_missed_trains(s))