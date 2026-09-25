import sys
from collections import Counter

def main():
    import sys
    from collections import Counter

    def main():
        import sys
        from collections import Counter

        n = int(sys.stdin.readline().strip())
        strings = [sys.stdin.readline().strip() for _ in range(2 * n - 2)]

        # Count occurrences of each string
        count = Counter(strings)

        # Sort strings by their length and lexicographical order
        strings.sort(key=lambda x: (len(x), x))

        result = []

        # Assign 'P' or 'S' based on the frequency and position
        for s in strings:
            if count[s] == 1:
                # Unique strings are likely to be either all prefixes or all suffixes
                result.append('P')
            else:
                # Non-unique strings need to be balanced between prefixes and suffixes
                if len(result) < n - 1:
                    result.append('P')
                else:
                    result.append('S')

        print(''.join(result))

    if __name__ == "__main__":
        main()

if __name__ == "__main__":
    main()