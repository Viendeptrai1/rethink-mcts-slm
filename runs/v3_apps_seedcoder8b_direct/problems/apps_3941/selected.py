def can_unlock_all_doors(n, m, room_status, switches):
    from collections import defaultdict

    # Create a mapping of each room to the switches that control it
    room_to_switches = defaultdict(list)
    for switch_index, switch in enumerate(switches):
        for room in switch[1:]:
            room_to_switches[room].append(switch_index)

    # Create a list to track the number of toggles needed for each room
    toggle_count = [0] * n

    # Calculate the toggle count for each room
    for room in range(1, n + 1):
        if room_status[room - 1] == 0:  # If the room is locked
            if len(room_to_switches[room]) != 2:
                return "NO"
            toggle_count[room - 1] += 1

    # Check if toggling the switches can unlock all doors
    for room in range(1, n + 1):
        if toggle_count[room - 1] % 2 != 0:
            return "NO"

    return "YES"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    room_status = list(map(int, data[2:n+2]))
    
    switches = []
    index = n + 2
    for _ in range(m):
        x_i = int(data[index])
        switch = [x_i] + list(map(int, data[index+1:index+1+x_i]))
        switches.append(switch)
        index += 1 + x_i
    
    result = can_unlock_all_doors(n, m, room_status, switches)
    print(result)

if __name__ == "__main__":
    main()