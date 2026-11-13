def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        
        if n % 2 != 0:
            results.append("NO")
            continue
        
        half_n = n // 2
        
        # Generate the first half of the array with even numbers
        even_numbers = [2 * i for i in range(1, half_n + 1)]
        
        # Generate the second half of the array with odd numbers
        odd_numbers = [2 * i - 1 for i in range(1, half_n + 1)]
        
        # Check if the sum of the first half equals the sum of the second half
        if sum(even_numbers) == sum(odd_numbers):
            results.append("YES")
            results.append(" ".join(map(str, even_numbers + odd_numbers)))
        else:
            results.append("NO")
    
    sys.stdout.write("\n".join(results) + "\n")