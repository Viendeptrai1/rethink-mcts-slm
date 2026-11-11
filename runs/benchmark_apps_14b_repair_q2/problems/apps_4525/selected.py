def construct_array(n):
    if n == 2:
        return "NO"
    
    half = n // 2
    
    # Generate the first half with even numbers
    even_part = list(range(2, half * 2 + 1, 2))
    
    # Generate the second half with odd numbers
    odd_part = list(range(1, half * 2, 2))
    
    # Calculate the sums
    even_sum = sum(even_part)
    odd_sum = sum(odd_part)
    
    # Adjust the sums if they are not equal
    if even_sum != odd_sum:
        # Try to adjust the last element of the even part
        if even_sum > odd_sum:
            diff = even_sum - odd_sum
            if diff % 2 == 0:
                even_part[-1] += diff
            else:
                return "NO"
        else:
            diff = odd_sum - even_sum
            if diff % 2 == 0:
                odd_part[-1] += diff
            else:
                return "NO"
    
    # Combine both parts
    result = even_part + odd_part
    return "YES", result

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
        result = construct_array(n)
        results.append(result)
    
    for result in results:
        if result == "NO":
            print("NO")
        else:
            print("YES")
            print(" ".join(map(str, result[1])))

if __name__ == "__main__":
    main()