def find_beautiful_sequence(k, q):
    if len(q) < k:
        return "NO"
    
    used_chars = set()
    result = []
    
    for i in range(k):
        if i == k - 1:
            remaining = q[len(used_chars):]
            if all(char in used_chars for char in remaining):
                return "NO"
            result.append(remaining)
        else:
            for j in range(len(q), 0, -1):
                prefix = q[:j]
                if prefix[0] not in used_chars and len(prefix) <= len(q) - len(used_chars):
                    used_chars.add(prefix[0])
                    result.append(prefix)
                    break
    
    return "YES\n" + "\n".join(result)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

k = int(data[0])
q = data[1]

print(find_beautiful_sequence(k, q))