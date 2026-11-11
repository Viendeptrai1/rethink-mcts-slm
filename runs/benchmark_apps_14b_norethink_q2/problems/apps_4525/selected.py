import sys

def solve(n):
    if n == 2:
        return "NO"
    
    half = n // 2
    
    # Generate the first half with even numbers
    even_half = list(range(2, half * 2 + 1, 2))
    
    # Generate the second half with odd numbers
    odd_half = list(range(1, half * 2 + 1, 2))
    
    # Check if the sums are equal
    if sum(even_half) != sum(odd_half):
        return "NO"
    
    return "YES", even_half + odd_half

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
            results.extend(result[1])
    
    for result in results:
        if isinstance(result, list):
            print(" ".join(map(str, result)))
        else:
            print(result)

if __name__ == "__main__":
    main()