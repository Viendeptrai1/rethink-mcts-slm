def count_equal_f_values(n, sequence):
    def f(x):
        result = 0
        while x > 0:
            if x % 2 == 1:
                result += 1
            x //= 2
        return result

    f_values = [f(x) for x in sequence]
    count_map = {}

    for value in f_values:
        if value in count_map:
            count_map[value] += 1
        else:
            count_map[value] = 1

    count_pairs = 0
    for count in count_map.values():
        if count > 1:
            count_pairs += count * (count - 1) // 2

    return count_pairs

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    sequence = list(map(int, data[1:n+1]))
    
    result = count_equal_f_values(n, sequence)
    print(result)