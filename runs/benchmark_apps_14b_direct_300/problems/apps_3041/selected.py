import sys

def min_coupons(N, trips):
    coupons = 0
    current_ticket = None
    
    for Z, T in trips:
        if current_ticket is None or Z < current_ticket[0] or Z > current_ticket[1] or T >= current_ticket[2]:
            # Calculate the cost of a new ticket
            if Z == 0:
                A, B = 0, 0
            else:
                A, B = 0, Z
            cost = 2 + abs(A - B)
            coupons += cost
            current_ticket = (A, B, T + 10000)
    
    return coupons

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    trips = []
    index = 1
    for i in range(N):
        Z = int(data[index])
        T = int(data[index + 1])
        trips.append((Z, T))
        index += 2
    
    result = min_coupons(N, trips)
    print(result)

if __name__ == "__main__":
    main()