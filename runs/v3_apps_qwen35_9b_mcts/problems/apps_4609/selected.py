import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    a = [int(x) for x in data[1:]]
    
    sheet = set()
    for x in a:
        if x in sheet:
            sheet.remove(x)
        else:
            sheet.add(x)
    
    print(len(sheet))

if __name__ == "__main__":
    solve()