import sys
from collections import defaultdict

def parse_molecule(molecule):
    stack = []
    count = defaultdict(int)
    i = 0
    while i < len(molecule):
        if molecule[i].isalpha():
            j = i + 1
            while j < len(molecule) and molecule[j].isdigit():
                j += 1
            num = int(molecule[i+1:j]) if j > i + 1 else 1
            count[molecule[i]] += num
            i = j
        elif molecule[i] == '(':
            stack.append(count.copy())
            count = defaultdict(int)
            i += 1
        elif molecule[i] == ')':
            j = i + 1
            while j < len(molecule) and molecule[j].isdigit():
                j += 1
            num = int(molecule[i+1:j]) if j > i + 1 else 1
            for key in count:
                count[key] *= num
            prev_count = stack.pop()
            for key in count:
                prev_count[key] += count[key]
            count = prev_count
            i = j
    return count

def max_output(input_molecule, input_count, output_molecule):
    input_counts = [parse_molecule(input_molecule) for _ in range(input_count)]
    output_counts = parse_molecule(output_molecule)
    
    min_ratio = float('inf')
    for element, count in output_counts.items():
        total_input_count = sum(mol[element] for mol in input_counts)
        if total_input_count < count:
            return 0
        min_ratio = min(min_ratio, total_input_count // count)
    
    return min_ratio

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    input_molecule, input_count = data[0].split()
    input_count = int(input_count)
    output_molecule = data[1]
    
    result = max_output(input_molecule, input_count, output_molecule)
    print(result)

if __name__ == "__main__":
    main()