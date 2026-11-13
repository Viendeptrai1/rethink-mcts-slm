from typing import List

def check_lexicographical_order(s: str, t: str) -> bool:
    # Count the frequency of each character in both strings
    count_s = [0] * 26
    count_t = [0] * 26
    
    for char in s:
        count_s[ord(char) - ord('a')] += 1
    
    for char in t:
        count_t[ord(char) - ord('a')] += 1
    
    # Compare the strings lexicographically
    for i in range(26):
        if count_s[i] < count_t[i]:
            return True
        elif count_s[i] > count_t[i]:
            return False
    
    # If all counts are equal, the strings cannot be made lexicographically smaller
    return False

# Main function to read input and print the result
def main():
    s = input().strip()
    t = input().strip()
    
    if check_lexicographical_order(s, t):
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()