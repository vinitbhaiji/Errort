list_dict={1:[0,0,0,0,0,0,0],2:[0,0,0,0,0,0,0]}
flag=0
i=0
j=0
k=0
def update():
    global flag,i,j,k
    check=False
    if flag==3:
        check=True
    x=0
    if flag==1:
        x=i
        list_dict[x][0]=1
        list_dict[x][1]=1
        list_dict[x][2]=1
    elif flag==2:
        x=j
        list_dict[x][3]=1
    elif flag==3:
        x=k
        list_dict[x][4]=1
        list_dict[x][5]=1
        list_dict[x][6]=1

    flag=0
    print(list_dict)
    if check==True:
        print(list_dict)
        print("Deleting : ",list_dict[x])
        for c in range(k,len(list_dict)):
            list_dict[c]=list_dict[c+1]
        del list_dict[len(list_dict)]
        i-=1
        j-=1
        k-=1
        print(list_dict)
        print("OK")

while True:
    flag=int(input("Enter flag"))
    if flag==1:
        i+=1
        list_dict[i]=[0,0,0,0,0,0,0]
    if flag==2:
        j+=1
    if flag==3:
        k+=1
    update()