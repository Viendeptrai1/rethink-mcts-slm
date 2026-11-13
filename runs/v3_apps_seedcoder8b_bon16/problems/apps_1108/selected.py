def count_rooms_with_free_place_for_george_and_alex(n, rooms):
    count = 0
    for p_i, q_i in rooms:
        if p_i + 2 <= q_i:
            count += 1
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    n = int(data[0])
    rooms = [tuple(map(int, data[i+1].split())) for i in range(n)]
    
    result = count_rooms_with_free_place_for_george_and_alex(n, rooms)
    print(result)

if __name__ == "__main__":
    main()