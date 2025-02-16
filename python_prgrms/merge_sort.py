
def mergeSort(lst,l,r):
    if l<r:
        m=(l+r)//2
        print('in ms',lst,l,m,r)
        mergeSort(lst,l,m)
        print('going to r',m+1,r)
        mergeSort(lst,m+1,r)
        print('going to merge',l,r)
        merge(lst,l,m,r)
    else:
        print('done',l,r)

def merge(lst,l,m,r):
    print('in merge',lst,l,m,r)
    temp=[0]*(r-l+1)
    print('ltemp',len(temp))
    i=l
    j=m+1
    k=0
    print('ijk',i,j,k)
    print('lmr',l,m,m+1,r,lst)
    while i<=m and j<=r:
        if lst[i]<lst[j]:
            print(i,j,k)
            temp[k]=lst[i]
            i+=1
            k+=1
        else:
            temp[k]=lst[j]
            j+=1
            k+=1
    print(temp)
    while i<=m:
        temp[k]=lst[i]
        i+=1
        k+=1
    while j<=r:
        temp[k]=lst[j]
        j+=1
        k+=1
    for i in range(0,k):
        lst[l+i]=temp[i]
    print('merged',temp,lst)
        
lst=list(map(int,input().split()))
n=len(lst)
mergeSort(lst,0,n-1)

