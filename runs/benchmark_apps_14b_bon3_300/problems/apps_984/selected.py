class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def build_tree(nodes, index):
    if index == -1:
        return None
    value, left_index, right_index = nodes[index]
    node = TreeNode(value)
    node.left = build_tree(nodes, left_index)
    node.right = build_tree(nodes, right_index)
    return node

def find(node, x):
    if node is None:
        return False
    if node.value == x:
        return True
    if x < node.value:
        return find(node.left, x)
    else:
        return find(node.right, x)

def count_fails(root, values):
    fail_count = 0
    for value in values:
        if not find(root, value):
            fail_count += 1
    return fail_count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    nodes = []
    for i in range(n):
        value = int(data[3 * i + 1])
        left_index = int(data[3 * i + 2])
        right_index = int(data[3 * i + 3])
        nodes.append((value, left_index, right_index))
    
    root = build_tree(nodes, 0)
    values = [node[0] for node in nodes]
    
    result = count_fails(root, values)
    print(result)

if __name__ == "__main__":
    main()