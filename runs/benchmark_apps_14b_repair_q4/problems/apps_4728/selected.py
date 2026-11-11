import sys

def parse_molecule(molecule):
    from collections import defaultdict
    stack = []
    count = defaultdict(int)
    i = 0
    while i < len(molecule):
        if molecule[i].isalpha():
            j = i + 1
            while j < len(molecule) and molecule[j].isdigit():
                j += 1
            num = int(molecule[i+1:j]) if j > i + 1 else 1
            stack.append((molecule[i], num))
            i = j
        elif molecule[i] == '(':
            stack.append('(')
            i += 1
        elif molecule[i] == ')':
            j = i + 1
            while j < len(molecule) and molecule[j].isdigit():
                j += 1
            num = int(molecule[i+1:j]) if j > i + 1 else 1
            temp_count = defaultdict(int)
            while stack[-1] != '(':
                atom, cnt = stack.pop()
                temp_count[atom] += cnt
            stack.pop()  # pop '('
            for atom, cnt in temp_count.items():
                stack.append((atom, cnt * num))
            i = j
    for atom, cnt in stack:
        count[atom] += cnt
    return count

def max_output_molecules(input_molecule, k, output_molecule):
    input_count = parse_molecule(input_molecule)
    output_count = parse_molecule(output_molecule)
    
    max_molecules = float('inf')
    for atom, cnt in output_count.items():
        if atom not in input_count:
            return 0
        max_molecules = min(max_molecules, input_count[atom] // (cnt * k))
    
    return max_molecules

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    input_molecule = data[0]
    k = int(data[1])
    output_molecule = data[2]
    
    result = max_output_molecules(input_molecule, k, output_molecule)
    print(result)

if __name__ == "__main__":
    main()