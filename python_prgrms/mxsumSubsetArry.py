import sys
def maxSubarray(n,lst):
    maxsum=-sys.maxsize-1
    for i in range(0,n):
        insum=lst[i]
        for j in range(i+1,n):
            insum=insum+lst[j]
            maxsum=max(maxsum,insum)
    print(maxsum)

n=16
lst=[5,7,-1,-15,8,2,-5,7,4,-1,10,-45,3,12,-1,2,-3]
maxSubarray(n,lst)