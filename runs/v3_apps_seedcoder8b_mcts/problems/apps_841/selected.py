def find_sequence_for_1337_subsequences(t, queries):
    results = []
    for n in queries:
        # The sequence '1337' itself is a subsequence
        # We need to repeat '1337' n times to ensure we have exactly n subsequences
        # Since '1337' is 4 characters long, repeating it n times will give us n subsequences
        sequence = '1337' * n
        results.append(sequence)
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    queries = list(map(int, data[1:t+1]))
    
    results = find_sequence_for_1337_subsequences(t, queries)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()