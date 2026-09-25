import sys

def min_days_to_write_coursework(n, m, a):
    a.sort(reverse=True)
    days = 0
    remaining_pages = m
    
    while remaining_pages > 0:
        days += 1
        written_pages = 0
        for i in range(len(a)):
            if a[i] > 0:
                written_pages += max(0, a[i] - i)
                a[i] -= 1
            if written_pages >= remaining_pages:
                break
        if written_pages < remaining_pages:
            return -1
        remaining_pages -= written_pages
    
    return days

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    
    result = min_days_to_write_coursework(n, m, a)
    print(result)

if __name__ == "__main__":
    main()