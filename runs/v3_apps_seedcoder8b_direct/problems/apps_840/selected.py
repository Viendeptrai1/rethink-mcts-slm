def max_cookies(n, k, a, b):
    # Calculate the difference needed for each ingredient to reach the requirement of one cookie
    difference = [a[i] - b[i] for i in range(n)]
    
    # Sort the differences to prioritize using magic powder on the ingredients that need more
    difference.sort()
    
    cookies = 0
    for diff in difference:
        if diff > 0:
            # If the difference is positive, we can't make any cookies with this ingredient
            continue
        # Calculate how many cookies we can make with the current ingredient
        cookies_to_make = min(-diff, k)
        cookies += cookies_to_make
        k -= cookies_to_make
        if k == 0:
            break
    
    return cookies

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:n+2]))
    b = list(map(int, data[n+2:2*n+2]))
    
    result = max_cookies(n, k, a, b)
    print(result)

if __name__ == "__main__":
    main()