import sys

def is_substring_of_any(s, processed_strings):
    for ps in processed_strings:
        if s in ps:
            return True
    return False

def can_reorder_strings(strings):
    processed_strings = []
    for s in strings:
        if is_substring_of_any(s, processed_strings):
            processed_strings.append(s)
        else:
            return False
    return True

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    if can_reorder_strings(strings):
        print("YES")
        print("\n".join(strings))
    else:
        print("NO")

if __name__ == "__main__":
    main()