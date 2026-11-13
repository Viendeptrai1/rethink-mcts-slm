import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = []
    for i in range(n):
        a.append(int(data[1 + i]))
    
    # We need to find the minimum number of insertions.
    # This is equivalent to finding the maximum number of elements we can keep 
    # such that no subsegment of the kept elements sums to 0, and then subtracting that count from n.
    # However, a more direct greedy approach works:
    # We iterate through the array and maintain a set of prefix sums of the "kept" sequence.
    # If adding the current element would create a prefix sum that we have seen before (which implies a subsegment sum of 0),
    # we must "break" the sequence by inserting a number. Breaking means we reset our prefix sum set and start counting a new segment.
    # The number of insertions is the number of times we break.
    
    seen = set()
    current_sum = 0
    insertions = 0
    
    for x in a:
        current_sum += x
        if current_sum in seen:
            # Found a subsegment with sum 0 ending at current position.
            # We must insert a number before this element to break the chain.
            # Effectively, we reset the prefix sum tracking for the next segment.
            # The inserted number breaks the continuity, so the new segment starts fresh.
            insertions += 1
            seen = set()
            current_sum = 0
        else:
            seen.add(current_sum)
    
    print(insertions)

if __name__ == '__main__':
    solve()