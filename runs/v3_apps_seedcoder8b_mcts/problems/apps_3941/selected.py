def can_unlock_all_doors(n, m, room_status, switches):
    from collections import defaultdict

    # Create a dictionary to track the effect of each switch on each room
    switch_effect = defaultdict(lambda: [0, 0])

    # Process each switch
    for i in range(m):
        switch = switches[i]
        num_rooms = switch[0]
        rooms = switch[1:]
        for room in rooms:
            switch_effect[room][i % 2] += 1

    # Check the parity of the effect on each room
    for room in range(1, n + 1):
        if room_status[room - 1] == 0:  # If the room is initially locked
            # If the room is toggled an odd number of times, it will remain locked
            if (switch_effect[room][0] + switch_effect[room][1]) % 2 == 0:
                return "NO"

    return "YES"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    room_status = list(map(int, data[2:n + 2]))
    
    switches = []
    index = n + 2
    for _ in range(m):
        x_i = int(data[index])
        rooms = list(map(int, data[index + 1:index + 1 + x_i]))
        switches.append([x_i] + rooms)
        index += 1 + x_i
    
    result = can_unlock_all_doors(n, m, room_status, switches)
    print(result)

if __name__ == "__main__":
    main()