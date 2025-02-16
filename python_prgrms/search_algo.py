#Binary search interative
def binary_Search(lst,k):
    n=len(lst)
    lst.sort()
    l=0
    r=n-1
    while l<=r:
        m=(l+r)//2
        if lst[m]==k:
            return True
        elif lst[m]>k:
            r=m-1
        else:
            l=m+1
    return False

lst=[5,10,-3,8,12,15,1,-7,18]
k=-12
print(binary_Search(lst,k))

#recursive 
def binary_Search(lst,l,r,k):
    m=(l+r)//2
    if lst[m]==k:
        return True
    elif lst[m]>k and l<r:
        return binary_Sort(lst,l,m-1,k)
    elif lst[m]<k and l<r:
        return binary_Sort(lst,m+1,r,k)
    else:
        return False

lst=[5,10,-3,8,12,15,1,-7,18]
n=len(lst)
k=-12
l=0
r=n-1
print(binary_Search(lst,l,r,k))


#Binary search interative
def binary_Search(lst,k,i):
    n=len(lst)
    l=0
    r=n-1
    while l<=r:
        m=(l+r)//2
        if lst[m]==k:
            return True
        elif lst[m]>k:
            r=m-1
        else:
            l=m+1
    return False
def sum_K(lst,n,k):
    lst.sort()
    print(lst)
    ans=[]
    for i in range(0,n-1):
        b=k-lst[i]
        res=binary_Search(lst[i+1:],b,i)
        if res:
           ans.append((lst[i],b)) 
    print(ans)
           
lst=[5,10,-3,8,12,15,1,-7,18]
n=len(lst)
k=23
sum_K(lst,n,k)

#Finding Floor
#nearest max number <=k. K may or may not exist in list
'''e.g. 
i/p-o/p
17-15,
7-5,
30-25,
5-5,
-10- -infinite'''
import sys
def max_Bsr(lst,k):
    n=len(lst)
    l=0
    r=n-1
    ans=-sys.maxsize-1
    while (l<=r) :
        m=(l+r)//2
        if lst[m]<=k:
            ans=lst[m]
            l=m+1
        else: 
            r=m-1
    return ans

lst=[-6,-3,-1,2,5,12,15,18,25]
k=-3
print(max_Bsr(lst,k))

#=================== FREQUENCY OF NUMBER =======================#
# find out how many times the number has occurred in list. 
lst=[5,1,8,1,5,3,15,5,5,20,18,5,8,10,10,10]

#*** BRUTE FORCE ***
def find_Freq(lst,k):
    n=len(lst)
    lst.sort()
    print(lst)
    cnt=0
    flag=False
    for i in lst:
        if i==k:
            cnt+=1
            flag=True
        else:
            flag=False
        if flag is False and cnt>0:
            break
    return cnt


lst=[5,1,8,1,5,3,15,5,5,20,18,5,8,10,10,10]
k=20
print(find_Freq(lst,k))

#**** Binary Search - approach two *** # 
def freq_Count(lst,k):
    lst.sort()
    n=len(lst)
    print(lst)
    cnt=0
    l=0
    r=n-1
    idx=-1
    while (l<=r):
        m=(l+r)//2
        if lst[m]==k:
            idx=m
            break
        elif lst[m]>k:
            r=m-1
        else:
            l=m+1
    if idx==-1:
        return cnt
    while (m<n and lst[m]==k):
        cnt+=1
        m+=1
    m=idx
    while (m>=0 and lst[m]==k):
        cnt+=1
        m-=1
    return cnt-1
lst=[5,1,8,1,5,3,15,5,5,20,18,5,8,10,10,10]
#lst1=[3,3,3,3,3,3,3,3,3,3]
k=3
print(freq_Count(lst,k))

#********** Binary Search -- Approach three **** #
def freq_Count(lst,n,k):
    print(lst,k)
    p1=bsr_Right(lst,n,k)
    if p1==-1:
        return 0
    p2=bsr_Left(lst,n,k)
    res=p1-p2+1
    return res
def bsr_Right(lst,n,k):
    l=0
    r=n-1
    idx=-1
    while (l<=r):
        m=(l+r)//2
        if lst[m]==k:
            idx=m
            l=m+1
        elif lst[m]>k:
            r=m-1
        else:
            l=m+1
    return idx
def bsr_Left(lst,n,k):
    l=0
    r=n-1
    idx=-1
    while (l<=r):
        m=(l+r)//2
        if lst[m]==k:
            idx=m
            r=m-1
        elif lst[m]>k:
            r=m-1
        else:
            l=m+1
    return idx
#lst=[5,1,8,1,5,3,15,5,5,20,18,5,8,10,10,10]
lst=[3,3,3,3,3,3,3,3,3,3]
k=3
lst.sort()
n=len(lst)
print(freq_Count(lst,n,k))

#******* approach-4 without BSR  *****
def count_Element(lst,n,k):
    print(lst)
    elst=[]
    clst=[]
    cnt=1
    for i in range(0,n-1):
        if lst[i]==lst[i+1]:
            cnt+=1
        else:
            elst.append(lst[i])
            clst.append(cnt)
            cnt=1
    elst.append(lst[-1])
    if lst[-1]==lst[-2]:
        clst.append(cnt)
    else:
        clst.append(1)
    print(elst,clst)
#lst=[5,1,8,1,5,3,15,5,5,20,18,5,8,10,10,10]
lst=[3,3,3,3,3,3,3,3,3,3]
k=5
lst.sort()
n=len(lst)
count_Element(lst,n,k)

