import math
def fearPrimeList(plst):
    fplst=plst[:]
    for i in range(0,1000000):
        if plst[i]==1:
            fp=str(i)
            fpn=len(fp)
            if '0' not in fp:
                j=0
                flag=True
                while j<fpn:
                    if plst[int(fp[j:])]==1:
                        j+=1
                    else:
                        flag=False
                        break
            else:
                flag=False
            if flag is True:
                print(fp)
                fplst[int(fp)]=1
    return fplst
t=int(input())
n=1000000
plst=[1]*(n+1)
plst[0]=0
plst[1]=0
sn=int(math.sqrt(n)+1)
for i in range(2,sn):
    if plst[i]==1:
        k=2
        while i*k<n+1:
            plst[i*k]=0
            k=k+1
print('plst is done')
flst=fearPrimeList(plst)
for _ in range(t):
    p=int(input())
    print(sum(flst[:p+1]))