def find_beautiful_sequence(k, q):
    if len(q) < k:
        return "NO"
    
    used_chars = set()
    result = []
    
    for i in range(k):
        for j in range(i, len(q)):
            if q[j] not in used_chars:
                result.append(q[i:j+1])
                used_chars.add(q[j])
                break
        else:
            return "NO"
    
    return "YES\n" + "\n".join(result)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

k = int(data[0])
q = data[1]

print(find_beautiful_sequence(k, q))