import sys

def is_valid(res, s, t):
    return s not in res and t not in res

def backtrack(n, s, t, current, count_a, count_b, count_c):
    if len(current) == 3 * n:
        return current if is_valid(current, s, t) else None
    
    if count_a < n:
        result = backtrack(n, s, t, current + 'a', count_a + 1, count_b, count_c)
        if result:
            return result
    
    if count_b < n:
        result = backtrack(n, s, t, current + 'b', count_a, count_b + 1, count_c)
        if result:
            return result
    
    if count_c < n:
        result = backtrack(n, s, t, current + 'c', count_a, count_b, count_c + 1)
        if result:
            return result
    
    return None

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    result = backtrack(n, s, t, "", 0, 0, 0)
    
    if result:
        print("YES")
        print(result)
    else:
        print("NO")

if __name__ == "__main__":
    main()