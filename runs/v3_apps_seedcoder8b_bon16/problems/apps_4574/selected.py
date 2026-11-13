def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort()
    max_area = 0
    
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            left = j + 1
            right = n - 1
            
            while left < right:
                width = min(a[j] - a[i], a[right] - a[left])
                height = min(a[left] - a[i], a[right] - a[j])
                area = width * height
                max_area = max(max_area, area)
                
                if width < height:
                    left += 1
                else:
                    right -= 1
    
    print(max_area)

solve()