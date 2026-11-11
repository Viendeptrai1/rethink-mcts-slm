import sys

def most_frequent_two_gram(n, s):
    max_count = 0
    most_frequent = ""
    
    for i in range(n - 1):
        two_gram = s[i:i+2]
        count = s.count(two_gram)
        
        if count > max_count:
            max_count = count
            most_frequent = two_gram
    
    return most_frequent

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = most_frequent_two_gram(n, s)
    print(result)