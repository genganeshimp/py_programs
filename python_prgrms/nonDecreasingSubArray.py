import sys
def validLst(n,lst,i):
    prev=-sys.maxsize-1
    for j in range(0,n)[::-1]:
        if (i>>j)&1==1:
            if lst[n-1-j]<prev:
                return False
            prev=lst[n-1-j]
    return True
    
def nonDecreaseArray(n,lst):
    cnt=0
    print(1<<n)
    for i in range(1,1<<n):
        if validLst(n,lst,i):
            print('valid',i,format(i,'b'))
            cnt+=1
    return cnt
n=7
lst=[5,7,-2,10,3,15,7]
print(nonDecreaseArray(n,lst))