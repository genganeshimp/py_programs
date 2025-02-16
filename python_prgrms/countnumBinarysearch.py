def countOccurrences(lst,x,n):
    i=numCount(lst,x,n,True)
    if i==-1:
        return 0
    j=numCount(lst,x,n,False)
    return j-i+1


def numCount(lst,x,n,lrcheck):
    l=0
    r=n-1
    res=-1
    while l<=r:
        mid=(l+r)//2
        if lst[mid]==x:
            if lrcheck:
                r=mid-1
                res=mid
            else:
                l=mid+1
                res=mid
        elif lst[mid]>x:
            r=mid-1
        else:
            l=mid+1
    return res

lst=[1,2,2,3,4,4,4,4,5,5,6,7]
n=len(lst)
x=1
print(countOccurrences(lst,x,n))