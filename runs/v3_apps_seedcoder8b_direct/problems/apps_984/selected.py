class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def build_tree(n, vertices):
    nodes = [None] * n
    for i in range(n):
        v, l, r = vertices[i]
        nodes[i] = TreeNode(v)
        if l != -1:
            nodes[i].left = nodes[l]
        if r != -1:
            nodes[i].right = nodes[r]
    return nodes[0]

def find(t, x):
    if t is None:
        return False
    if t.value == x:
        return True
    if x < t.value:
        return find(t.left, x)
    else:
        return find(t.right, x)

def count_failed_searches(root, values):
    failed_count = 0
    for value in values:
        if not find(root, value):
            failed_count += 1
    return failed_count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    vertices = []
    index = 1
    for _ in range(n):
        v = int(data[index])
        l = int(data[index + 1])
        r = int(data[index + 2])
        vertices.append((v, l, r))
        index += 3
    
    root = build_tree(n, vertices)
    
    values = [v for v, _, _ in vertices]
    
    result = count_failed_searches(root, values)
    print(result)

if __name__ == "__main__":
    main()