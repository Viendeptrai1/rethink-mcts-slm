def min_abs_destination(X, K, D):
    # Calculate the net effect of K moves
    net_effect = K % 2 * D
    
    # Calculate the minimum possible absolute value of the destination
    min_abs_value = min(abs(X + net_effect), abs(X - net_effect))
    
    return min_abs_value

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    X, K, D = map(int, data.split())
    print(min_abs_destination(X, K, D))