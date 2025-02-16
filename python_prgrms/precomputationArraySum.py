'''
Given an array of integers, answer queries of the form: [i, j] : Print the sum of array elements from A[i] to A[j], both inclusive.
i/p
10
1 30 13 -4 -5 12 -53 -12 43 100 
4
0 5
1 7
2 3
7 9
output
47
-19
9
131
'''
n=int(input())
lst=list(map(int,input().split()))
slst=[0]*n
isum=0
for l in range(0,n):
    isum=isum+lst[l]
    slst[l]=isum
q=int(input())
for _ in range(q):
    i,j=map(int,input().split())
    if i!=0:
        print(slst[j]-slst[i-1])
    else:
        print(slst[j])
        
        