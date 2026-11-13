import sys

def is_lucky(h, m):
    s = f"{h:02d}{m:02d}"
    return '7' in s

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    x = int(input_data[0])
    hh = int(input_data[1])
    mm = int(input_data[2])
    
    count = 0
    while True:
        if is_lucky(hh, mm):
            print(count)
            return
        
        mm -= x
        if mm < 0:
            mm += 60
            hh -= 1
            if hh < 0:
                hh = 23
        
        count += 1

if __name__ == "__main__":
    solve()