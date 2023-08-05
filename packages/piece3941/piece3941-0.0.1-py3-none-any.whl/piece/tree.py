# -*- coding: utf-8 -*-
from bisect import bisect
import pygraphviz as pgv
from collections import defaultdict


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.val)


def deserialize(data):
    if not data:
        return None
    nodes = [None if val is None else TreeNode(val) for val in data]
    s = 0
    e = 1
    while True:
        layer = [node for node in nodes[s:e] if node is not None]
        if not layer:
            break
        for i in range(len(layer)):
            node = layer[i]
            if e + 2 * i < len(nodes):
                node.left = nodes[e + 2 * i]
            if e + 2 * i + 1 < len(nodes):
                node.right = nodes[e + 2 * i + 1]
        s = e
        e = e + 2 * len(layer)
    return nodes[0]


def serialize(root):
    if not root:
        return []
    container = [root]
    r = []
    while container:
        node = container.pop()
        if node:
            container = [node.right, node.left] + container
        r.append(node if node is None else node.val)
    return r


def build_from_middle_pre(middle, pre):

    def build_tree(middle, pre):
        if not middle:
            return None
        node = TreeNode(pre.pop(0))
        i = middle.index(node.val)
        node.left = build_tree(middle[:i], pre[:len(middle[:i])])
        node.right = build_tree(middle[i + 1:], pre[len(middle[:i]):])
        return node

    if not middle or not pre or len(middle) != len(pre):
        return None

    return build_tree(middle, pre)
    
    
def print_tree(root, dot='TreeExample.dot', png='TreeExample.png'):
    if not root:
        print("Tree needs to be built.")
    container = [root]
    d = defaultdict(list)
    while container:
        node = container.pop(0)
        if node.left:
            container.append(node.left)
            d[node.val].append(node.left.val)
        if node.right:
            container.append(node.right)
            d[node.val].append(node.right.val)
        G = pgv.AGraph(d)
        G.layout()
        G.draw(png, prog='dot')
        G.write(dot)


def search_middle_order(node):
    if not node:
        return []
    return search_middle_order(node.left)+ [node.val] + search_middle_order(node.right)


def search_pre_order(node):
    if not node:
        return []
    return [node.val] + search_pre_order(node.left) + search_pre_order(node.right)


def search_post_order(node):
    if not node:
        return []
    return search_post_order(node.left) + search_post_order(node.right) + [node.val]


if __name__ == "__main__":


    # middle_order: left root right
    # pre_order: root left right
    # post_order: left right left

    preordered = [9, 7, 6, 4, 3, 5, 8, 15, 12, 10, 13]
    middle_ordered = [3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15]

    # preordered = [2, 1, 4, 3, 5]
    # middle_ordered = [1, 2, 3, 4, 5]

    root = build_from_middle_pre(middle_ordered, preordered)
    print_tree(root)


    deserialize([3,9,20,None,None,15,7])
    serialized = serialize(root)
    root = deserialize(serialized)

    print(search_middle_order(root))
    print(search_pre_order(root))
    print(search_post_order(root))



