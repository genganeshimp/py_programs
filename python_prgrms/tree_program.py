class Node:
    def __init__(self,key):
        self.left=None
        self.right=None
        self.val=key
def inorderOfTree(root):
    if root==None:
        return
    inorderOfTree(root.left)
    print(root.val,end=' ')
    inorderOfTree(root.right)
def preOrderOfTree(root):
    if root==None:
        return 
    print(root.val,end=' ')
    preOrderOfTree(root.left)
    preOrderOfTree(root.right)
def postOrderOfTree(root):
    if root==None:
        return 
    postOrderOfTree(root.left)
    postOrderOfTree(root.right)
    print(root.val,end=' ')
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
print('===Inorder==')
inorderOfTree(root)
print(end='\n')
print('===preorder==')
preOrderOfTree(root)
print(end='\n')
print('===postorder==')
postOrderOfTree(root)
