import sys

def max_path_length(v1, v2, t, d):
    if v1 == v2:
        return v1 * t
    
    if v1 < v2:
        # Increase speed up to v2
        increase_time = min((v2 - v1) // d, t - 1)
        remaining_time = t - increase_time
        max_speed = v1 + increase_time * d
        return (v1 + max_speed) * increase_time // 2 + max_speed * remaining_time
    
    # Decrease speed down to v2
    decrease_time = min((v1 - v2) // d, t - 1)
    remaining_time = t - decrease_time
    min_speed = v1 - decrease_time * d
    return (v1 + min_speed) * decrease_time // 2 + min_speed * remaining_time

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    v1 = int(data[0])
    v2 = int(data[1])
    t = int(data[2])
    d = int(data[3])
    
    result = max_path_length(v1, v2, t, d)
    print(result)

if __name__ == "__main__":
    main()