import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    c1 = int(data[0])
    c2 = int(data[1])
    c3 = int(data[2])
    c4 = int(data[3])
    
    n = int(data[4])
    m = int(data[5])
    
    a = list(map(int, data[6:6+n]))
    b = list(map(int, data[6+n:6+n+m]))
    
    total_cost = 0
    
    # Calculate the cost for buses
    bus_cost = 0
    for rides in a:
        if rides * c1 < c2:
            bus_cost += rides * c1
        else:
            bus_cost += c2
    
    if bus_cost > c3:
        bus_cost = c3
    
    # Calculate the cost for trolleys
    trolley_cost = 0
    for rides in b:
        if rides * c1 < c2:
            trolley_cost += rides * c1
        else:
            trolley_cost += c2
    
    if trolley_cost > c3:
        trolley_cost = c3
    
    # Total cost considering all options
    total_cost = min(bus_cost + trolley_cost, c4)
    
    print(total_cost)

if __name__ == "__main__":
    main()