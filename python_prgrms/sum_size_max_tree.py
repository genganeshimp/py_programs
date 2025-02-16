class Node:
    def __init__(self,key):
        self.left=None
        self.right=None
        self.val=key
def sizeWithoutglobal(root):
    if root==None:
        return 0
    return 1+sizeWithoutglobal(root.left)+sizeWithoutglobal(root.right)
def sumofTree(root):
    if root==None:
        return 0
    return root.val+sumofTree(root.left)+sumofTree(root.right)    
def maxofTree(root):
    if root==None:
        return -1
    return max(root.val,maxofTree(root.left),maxofTree(root.right))
root=Node(5)
root.left=Node(10)
root.right=Node(-3)
root.left.right=Node(12)
root.left.right.left=Node(4)
root.left.right.right=Node(-1)
root.right.left=Node(6)
root.right.right=Node(8)
root.right.right.left=Node(7)
root.right.right.left.right=Node(18)
print('===size with global variable==')
print(sizeWithoutglobal(root))
print('===sum of Tree===')
print(sumofTree(root))
print('====max of tree===')
print(maxofTree(root))



