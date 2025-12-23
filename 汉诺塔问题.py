
def f(num,a,c,b):
    if num==1:
        return print("move"+"1"+"from"+a+"to"+c)
    else:
        f(num - 1, a, b, c)
        print("move"+str(num)+"from"+a+"to"+c)
        f(num - 1, b, c, a)

n=int(input())
f(n,"A","C","B")