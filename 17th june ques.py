#QUESTION 1
l=['anant','hi','inder','hola','rav','manni','zoo','simar','poha']
l2=[i for i in l if len(i)<=4]
print(l2)

print('-----------')

#QUESTION 2
l=[i for i in range(20)]
print(l)
l2=["even" if i%2==0 else "odd" for i in l]
print(l2)

print("-----------")

#QUESTION 3
l=[i for i in range(1,1000) if i%7==0]
print(l)

print('------------')

#QUESTION 4
l="hello there!!!! how are you guys" 
count=0
for i in l:
    if i==" ":
        count+=1
print("Space count: ",count)

print("----------")

#QUESTION 5
l1=[1,2,3,4]
l2=[2,3,4,5]
c=[i for i in l1 for j in l2 if i==j]
print(c)