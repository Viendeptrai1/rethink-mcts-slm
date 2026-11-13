def solve(n):
    if n == 2:
        return "NO"
    
    even_sum = 0
    odd_sum = 0
    
    # Generate the first half with even numbers
    for i in range(1, n//2 + 1):
        even_sum += 2 * i
        yield 2 * i
    
    # Generate the second half with odd numbers
    for i in range(1, n//2 + 1):
        odd_sum += 2 * i - 1
        yield 2 * i - 1
    
    # Check if sums are equal
    if even_sum != odd_sum:
        return "NO"

# Main function to handle input and output
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
            results.append("YES\n" + " ".join(map(str, result)))
    
    print("\n".join(results))

if __name__ == "__main__":
    main()