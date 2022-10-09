
from curses.ascii import isalpha, isdigit


st=list('kjhuyhh23nbvgf'.strip(""))
print("The String in Alphabetic order :")

for i in range(0,len(st)):
    min=st[i]
    pos=i
    if isalpha(st[i]):
        for j in range(i+1,len(st)):
            if isdigit(st[j]):
                continue
            if min>st[j]:
                min=st[j]
                pos=j
    temp=st[i]
    st[i]=st[pos]
    st[pos]=temp
print("".join(st))
