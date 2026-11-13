def find_sequence_with_subsequences(n):
    # The string "1337" can be formed as:
    # 1. "1" + "337"
    # 2. "3" + "37"
    # 3. "37"
    # 4. "7"

    # To find the sequence we need to consider the contribution of each digit:
    # - "1" can be formed as a subsequence by itself and with "337".
    # - "3" can be formed as a subsequence by itself and with "37".
    # - "7" can be formed as a subsequence by itself.

    # By observation, the number of times "1337" appears depends on the count of the digits:
    # - We need at least 3 '3's and at least 1 '1'.
    # - The number of sequences is bounded by the limiting factor of '3's.

    # Pre-calculate how many sequences "1337" can be formed with specific numbers of each digit:
    # '3's can be chosen from positions 1, 2, 3, 4, 5, etc.
    # '1's can be chosen from positions in the remaining positions after choosing '3's.
    # '7's can be chosen from the last available position.

    # Let's construct the string by ensuring it has exactly `n` subsequences of "1337":

    sequence = ["1", "3", "3", "7"] * n
    return ''.join(sequence)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    for i in range(1, t + 1):
        n = int(data[i])
        result = find_sequence_with_subsequences(n)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()