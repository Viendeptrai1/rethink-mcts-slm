import sys

def most_frequent_two_gram(n, s):
    two_gram_count = {}
    
    for i in range(n - 1):
        two_gram = s[i:i+2]
        if two_gram in two_gram_count:
            two_gram_count[two_gram] += 1
        else:
            two_gram_count[two_gram] = 1
    
    max_count = max(two_gram_count.values())
    for two_gram, count in two_gram_count.items():
        if count == max_count:
            return two_gram

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    s = data[1]
    result = most_frequent_two_gram(n, s)
    print(result)