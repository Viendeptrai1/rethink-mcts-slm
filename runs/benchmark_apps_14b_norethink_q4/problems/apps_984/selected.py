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

def count_failed_searches(n, nodes):
    root = build_tree(nodes, 0)
    failed_count = 0
    for i in range(n):
        value, _, _ = nodes[i]
        if not find(root, value):
            failed_count += 1
    return failed_count

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
nodes = []
index = 1
for i in range(n):
    value = int(data[index])
    left_index = int(data[index + 1])
    right_index = int(data[index + 2])
    nodes.append((value, left_index, right_index))
    index += 3

result = count_failed_searches(n, nodes)
print(result)