def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    a = int(data[0])
    b = int(data[1])
    c = int(data[2])
    
    total_candies = a + b + c
    
    if total_candies % 2 != 0:
        print("No")
        return
    
    target = total_candies // 2
    
    if a == target or b == target or c == target:
        print("Yes")
        return
    
    if a + b == target or a + c == target or b + c == target:
        print("Yes")
        return
    
    print("No")

if __name__ == "__main__":
    main()