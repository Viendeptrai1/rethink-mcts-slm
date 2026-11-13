def solve():
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

        if n == 2:
            results.append("NO")
        else:
            results.append("YES")
            
            # Construct the first half with even numbers
            even_numbers = list(range(2, n // 2 * 2 + 1, 2))
            
            # Construct the second half with odd numbers
            odd_numbers = list(range(1, n // 2 * 2, 2))
            
            # Ensure all numbers are distinct
            if len(even_numbers) != len(set(even_numbers)) or len(odd_numbers) != len(set(odd_numbers)):
                results[-1] = "NO"
            else:
                # Check if the sum of both halves is equal
                if sum(even_numbers) != sum(odd_numbers):
                    results[-1] = "NO"

            # Print the result and the array
            if results[-1] == "YES":
                print(results[-1])
                print(*even_numbers + odd_numbers)
            else:
                print(results[-1])

if __name__ == "__main__":
    solve()