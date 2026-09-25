import sys

def can_be_sorted_by_swapping(s):
    n = len(s)
    # Check if the string can be sorted by swapping adjacent differently colored characters
    # We need to ensure that for every pair of adjacent characters, if they are out of order,
    # they must be of different colors.
    
    # Create a sorted version of the string
    sorted_s = sorted(s)
    
    # Try to color the string such that it can be sorted by swapping
    # We will use a greedy approach to assign colors
    color = [0] * n
    
    # Check if we can sort the string by swapping
    for i in range(n):
        if s[i] != sorted_s[i]:
            # Find the position of the correct character in the sorted string
            j = i
            while s[j] != sorted_s[i]:
                j += 1
            
            # Swap the characters to their correct positions
            while j > i:
                if color[j] == color[j - 1]:
                    # If the colors are the same, we need to change one of them
                    color[j] = 1 - color[j]
                s[j], s[j - 1] = s[j - 1], s[j]
                j -= 1
    
    # Check if the string is now sorted
    if s == sorted_s:
        return True, ''.join(map(str, color))
    else:
        return False, ""

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    possible, coloring = can_be_sorted_by_swapping(s)
    
    if possible:
        print("YES")
        print(coloring)
    else:
        print("NO")

if __name__ == "__main__":
    main()