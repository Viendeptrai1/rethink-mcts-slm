def find_optimal_ratings(n, a):
    a = sorted((a[i], i) for i in range(n))
    b = [0] * n
    used_ratings = set()
    current_rating = 1

    for required_rating, original_index in a:
        while current_rating in used_ratings:
            current_rating += 1
        b[original_index] = max(required_rating, current_rating)
        used_ratings.add(b[original_index])
        current_rating += 1

    return b

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    result = find_optimal_ratings(n, a)
    print(" ".join(map(str, result)))