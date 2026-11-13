from sys import stdin, stdout

def find_beautiful_sequence(k, q):
    # Check if it's possible to split the string into k parts with unique starting characters
    if len(q) % k != 0:
        return "NO"
    
    part_length = len(q) // k
    used_chars = set()
    result = []
    
    for i in range(k):
        start_char = q[i * part_length]
        if start_char in used_chars:
            return "NO"
        used_chars.add(start_char)
        
        end_index = (i + 1) * part_length
        result.append(q[i * part_length:end_index])
    
    return "\n".join(["YES"] + result)

# Main function to handle input and output
def main():
    k = int(stdin.readline().strip())
    q = stdin.readline().strip()
    result = find_beautiful_sequence(k, q)
    stdout.write(result + '\n')

# Call the main function
if __name__ == "__main__":
    main()