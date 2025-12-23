def inverse(num):
    return str(num)[::-1]

def prime(num):
    flag=True
    if num==1:
        return False
    for i in range(2,int(num**0.5)+1):
        if num%i==0:
            flag=False
            break
    return flag
Final=[]
M,N=input().split(" ")
for j in range(int(M),int(N)+1):
    if prime(int(inverse(j))) and prime(j):
        Final.append(str(j))
if len(Final)>0:
    print(",".join(Final))
else:
    print("No")