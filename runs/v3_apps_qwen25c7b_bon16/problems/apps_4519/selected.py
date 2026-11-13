from sys import stdin, stdout

def min_binary_string(s, k):
    n = len(s)
    count = [0] * 2
    for char in s:
        count[int(char)] += 1
    
    left_ones = 0
    right_zeros = count[1]
    result = list(s)
    
    for i in range(n):
        if result[i] == '1':
            if k >= right_zeros + left_ones:
                result[i], result[left_ones] = result[left_ones], result[i]
                left_ones += 1
                k -= right_zeros + left_ones - 1
                right_zeros -= 1
            elif k > 0:
                right_zeros -= 1
                k -= 1
        else:
            if k >= left_ones + right_zeros:
                result[i], result[n - 1 - right_zeros] = result[n - 1 - right_zeros], result[i]
                right_zeros += 1
                k -= left_ones + right_zeros - 1
                left_ones -= 1
            elif k > 0:
                left_ones -= 1
                k -= 1
                
    return ''.join(result)

def main():
    input = stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        k = int(data[index + 1])
        s = data[index + 2]
        index += 3
        
        result = min_binary_string(s, k)
        results.append(result)
        
    for result in results:
        stdout.write(result + '\n')

if __name__ == '__main__':
    main()