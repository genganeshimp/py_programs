#Finding closest sum of two element in two sorted arrays. 

import sys
def closeSum(arr,brr):
    an=len(arr)
    bn=len(arr)
    x=50
    cdiff=sys.maxsize
    print(cdiff)
    for i in range(0,an):
        for j in range(0,bn):
            abdiff=abs(arr[i]+brr[j]-x)
            if abdiff<cdiff:
                cdiff=abdiff
                la,ba=arr[i],brr[j]
    print(la,ba)
    return None

arr=[1, 4, 5, 7]
brr=[10, 20, 30, 40]
closeSum(arr,brr)