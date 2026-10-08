import sys

def solve(n):
    if n == 2:
        return "NO"
    
    half = n // 2
    even_sum = 0
    odd_sum = 0
    
    even_numbers = []
    odd_numbers = []
    
    i = 2
    while len(even_numbers) < half:
        even_numbers.append(i)
        even_sum += i
        i += 2
    
    i = 1
    while len(odd_numbers) < half:
        odd_numbers.append(i)
        odd_sum += i
        i += 2
    
    if even_sum != odd_sum:
        return "NO"
    
    return "YES", even_numbers + odd_numbers

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        result = solve(n)
        if result == "NO":
            results.append("NO")
        else:
            results.append("YES")
            results.extend(map(str, result[1]))
    
    print("\n".join(results))

if __name__ == "__main__":
    main()