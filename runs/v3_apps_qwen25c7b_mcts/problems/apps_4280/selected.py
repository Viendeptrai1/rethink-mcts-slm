import sys
from collections import defaultdict

def read_input():
    input = sys.stdin.read
    data = input().split()
    index = 0
    def next_int():
        nonlocal index
        result = int(data[index])
        index += 1
        return result
    n = next_int()
    k = next_int()
    roads = []
    for _ in range(n - 1):
        x = next_int()
        y = next_int()
        roads.append((x, y))
    return n, k, roads

def solve(n, k, roads):
    # Create adjacency list
    adj_list = defaultdict(list)
    for u, v in roads:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Initialize variables
    companies = {}
    company_count = 0
    
    # Function to check if a city is good
    def is_good_city(city):
        count = defaultdict(int)
        for neighbor in adj_list[city]:
            if neighbor in companies:
                count[companies[neighbor]] += 1
        return max(count.values()) <= 1
    
    # Assign roads to companies
    for i, (u, v) in enumerate(roads):
        if u not in companies and v not in companies:
            company_count += 1
            companies[u] = company_count
            companies[v] = company_count
        elif u in companies and v not in companies:
            companies[v] = companies[u]
        elif u not in companies and v in companies:
            companies[u] = companies[v]
        else:
            if len(adj_list[u]) > len(adj_list[v]):
                u, v = v, u
            if is_good_city(u):
                companies[v] = companies[u]
            else:
                company_count += 1
                companies[u] = company_count
                companies[v] = company_count
    
    # Output the result
    print(company_count)
    for i, (u, v) in enumerate(roads):
        print(companies[u], end=' ')
    print()

# Main function
if __name__ == "__main__":
    n, k, roads = read_input()
    solve(n, k, roads)