class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def build_tree(nodes):
    if not nodes:
        return None
    
    # Create a list of TreeNode objects
    tree_nodes = [TreeNode(node[0]) for node in nodes]
    
    # Build the tree structure
    for i, node in enumerate(nodes):
        value, left_index, right_index = node
        if left_index != -1:
            tree_nodes[i].left = tree_nodes[left_index - 1]
        if right_index != -1:
            tree_nodes[i].right = tree_nodes[right_index - 1]
    
    # Return the root of the tree
    return tree_nodes[0]

def find_failures(root, x):
    if root is None:
        return True
    if root.value == x:
        return False
    if x < root.value:
        return find_failures(root.left, x)
    else:
        return find_failures(root.right, x)

def count_search_failures(n, nodes):
    root = build_tree(nodes)
    failure_count = 0
    for node in nodes:
        value, _, _ = node
        if find_failures(root, value):
            failure_count += 1
    return failure_count

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
nodes = []
index = 1
for _ in range(n):
    value = int(data[index])
    left_index = int(data[index + 1])
    right_index = int(data[index + 2])
    nodes.append((value, left_index, right_index))
    index += 3

# Calculate and print the number of failures
print(count_search_failures(n, nodes))