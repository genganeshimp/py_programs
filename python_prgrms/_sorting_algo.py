https://www.geeksforgeeks.org/sorting-algorithms/
#bubble sort 
def bubble_Sort(alst):
    print(alst)
    n=len(alst)
    for i in range(n):
        flag=False
        for j in range(n-i-1):
            if alst[j]>alst[j+1]:
                alst[j],alst[j+1]=alst[j+1],alst[j]
                flag=True
        if flag is False:
            break
    return alst
alst=[3,8,2,15,10,10,-7]
print(bubble_Sort(alst))

#Insertion sort 
def insertion_Sort(lst,n):
    for i in range(1,n):
        key=lst[i]
        j=i-1
        while (j>=0 and key<lst[j]):
            lst[j+1]=lst[j]
            j-=1
        lst[j+1]=key
    return lst        

lst=[9,0,2,1,3,7,-5,6]
n=len(lst)
print(insertion_Sort(lst,n))

#selection sort solution 
def select_Sort(alst):
    print(alst)
    n=len(alst)
    for i in range(n):
        min_i=alst[i]
        for j in range(i,n):
            if alst[j]<min_i:
                min_i=alst[j]
                alst[j],alst[i]=alst[i],alst[j]
        print(i,j,min_i,alst)
    return alst
alst=[3,8,2,15,10,7]
print(select_Sort(alst))

#two pointer technique. 
#input
-1 2 5 7 8 9 11 
-9 -5 -3 3 4 6 13 12 24 43
def two_Pointer(a,b):
    an=len(a)
    bn=len(b)
    print(a,an)
    print(b,bn)
    p1=0
    p2=0
    res=[]
    while (p1<an)&(p2<bn):
        if a[p1]<b[p2]:
            res.append(a[p1])
            p1+=1
        else:
            res.append(b[p2])
            p2+=1
    while p1<an:
        res.append(a[p1])
        p1+=1
    while p2<bn:
        res.append(b[p2])
        p2+=1
    return res
alst=list(map(int,input().rstrip().split()))
blst=list(map(int,input().rstrip().split()))
print(two_Pointer(alst,blst))

def sort_ZeroOne(a):
    n=len(a)
    print(a,n)
    p1=0
    p2=n-1
    while (p1<p2):
        if (a[p1]==0) & (a[p2]==1):
            p1+=1
            p2-=1
        elif a[p1]==1:
            a[p1],a[p2]=a[p2],a[p1]
            p2-=1
        elif a[p2]==0:
            a[p1],a[p2]=a[p2],a[p1]
            p1+=1
    return a
alst=[1,1,0,1,0,0,0,0,1,1,0,0]
print(sort_ZeroOne(alst))


