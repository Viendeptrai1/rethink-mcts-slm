def min_transport_cost(c1, c2, c3, c4, n, m, a, b):
    total_rides_buses = sum(a)
    total_rides_trolleys = sum(b)

    # Option 1: Unlimited all-buses and all-trolleys ticket
    option1 = c4

    # Option 2: Unlimited all-buses ticket and unlimited all-trolleys ticket
    option2 = c3 + c3

    # Option 3: Unlimited all-buses ticket and individual trolley tickets
    option3 = c3 + sum(sorted(b)[::-1][:total_rides_trolleys])

    # Option 4: Unlimited all-trolleys ticket and individual bus tickets
    option4 = c3 + sum(sorted(a)[::-1][:total_rides_buses])

    # Option 5: Individual bus tickets and individual trolley tickets
    option5 = c1 * total_rides_buses + c1 * total_rides_trolleys

    return min(option1, option2, option3, option4, option5)

# Example usage:
if __name__ == "__main__":
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
    b = list(map(int, data[6+n:]))

    result = min_transport_cost(c1, c2, c3, c4, n, m, a, b)
    print(result)