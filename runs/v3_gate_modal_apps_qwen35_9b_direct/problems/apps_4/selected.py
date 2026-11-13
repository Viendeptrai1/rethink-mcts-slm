import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    x = int(input_data[0])
    hh = int(input_data[1])
    mm = int(input_data[2])
    
    def is_lucky(h, m):
        s = f"{h:02d}{m:02d}"
        return '7' in s
    
    count = 0
    while not is_lucky(hh, mm):
        mm -= x
        if mm < 0:
            mm += 60
            hh -= 1
            if hh < 0:
                hh = 23
        count += 1
    print(count)

if __name__ == "__main__":
    solve()