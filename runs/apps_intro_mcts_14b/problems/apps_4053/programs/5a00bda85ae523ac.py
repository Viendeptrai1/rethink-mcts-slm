import sys
from collections import defaultdict

def main():
    import sys
    from collections import defaultdict

    def main():
        import sys
        from collections import defaultdict

        n = int(sys.stdin.readline().strip())
        strings = [sys.stdin.readline().strip() for _ in range(2 * n - 2)]

        # Create a frequency map of the strings
        freq_map = defaultdict(int)
        for s in strings:
            freq_map[s] += 1

        # Identify unique patterns in prefixes and suffixes
        prefix_suffix_map = defaultdict(list)
        for i in range(n):
            prefix_suffix_map[strings[i]].append('P')
            prefix_suffix_map[strings[2 * n - 2 - i]].append('S')

        # Construct the result string
        result = []
        for s in strings:
            if len(prefix_suffix_map[s]) == 1:
                result.append(prefix_suffix_map[s][0])
            else:
                # If there are two possibilities, choose one arbitrarily
                result.append('P' if freq_map[s] == 1 else 'S')

        # Ensure the number of 'P' and 'S' are equal
        while result.count('P') != result.count('S'):
            for i in range(len(result)):
                if result[i] == 'P' and result.count('P') > result.count('S'):
                    result[i] = 'S'
                elif result[i] == 'S' and result.count('P') < result.count('S'):
                    result[i] = 'P'
                if result.count('P') == result.count('S'):
                    break

        print(''.join(result))

    if __name__ == "__main__":
        main()

if __name__ == "__main__":
    main()