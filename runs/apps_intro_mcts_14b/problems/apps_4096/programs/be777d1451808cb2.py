import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    
    total_caffeine = sum(a)
    if total_caffeine < m:
        print(-1)
        return
    
    a.sort(reverse=True)
    days = 0
    current_pages = 0
    
    while m > 0:
        days += 1
        for i in range(n):
            if a[i] == 0:
                continue
            current_pages += max(0, a[i] - days + 1)
            a[i] -= 1
            if current_pages >= m:
                break
        if current_pages < m:
            print(-1)
            return
    
    print(days)

if __name__ == "__main__":
    main()