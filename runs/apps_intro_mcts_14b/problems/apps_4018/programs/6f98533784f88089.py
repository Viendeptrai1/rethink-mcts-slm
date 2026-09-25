import sys

def min_cost_to_form_set(n, k, s):
    if k > 2**n:
        return -1
    
    # Calculate the cost to form k unique subsequences
    cost = 0
    current_subsequences = 1  # Start with the empty subsequence
    
    while current_subsequences < k:
        # Each new subsequence can be formed by adding one character to existing subsequences
        cost += n - (current_subsequences.bit_length() - 1)
        current_subsequences *= 2
    
    return cost

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    
    result = min_cost_to_form_set(n, k, s)
    print(result)

if __name__ == "__main__":
    main()