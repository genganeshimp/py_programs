#Selection Sort
def selectionSort(lst,n):
    
    for i in range(0,n):
        minidx=i
        minval=lst[i]
        for j in range(i+1,n):
            if lst[j]<minval:
                minidx=j
                minval=lst[j]
        lst[i],lst[minidx]=lst[minidx],lst[i]
        print(lst)
    return lst


t=int(input())
for _ in range(t):
    n=int(input())
    lst=list(map(int,input().rstrip().split()))
    print('-----------',selectionSort(lst,n))
    
#----------------input----------------------------#
6
8
176 -272 -272 -45 269 -327 -945 176 
2
-274 161 
7
274 204 -161 481 -606 -767 -351 
2
154 -109 
4
5 3 1 5 
4
40 10 20 40 


#other solution 
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