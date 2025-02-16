#finding 3 elements in list whose sum equals to x

def tripleSum(bl,n):
    x=22
    for i in range(n-2):
        for j in range(i+1,n-1):
            for k in range(j+1,n):
                if bl[i]+bl[j]+bl[k]==x:
                    print(bl[i],bl[j],bl[k])

    return None

bl=[1, 4, 45, 6, 10, 8]
n=len(bl)
tripleSum(bl,n)