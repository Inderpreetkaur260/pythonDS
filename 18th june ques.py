#QUESTION 1
t=(48,'hello',54,69,48,78,56,48,'hello',54,'hi',78,45)
print('Before: ',t)
t=set(t)
t=tuple(t)
print('Final tuple after removing duplicate elements: ',t)

print("------------")

#QUESTION 2
l1=[[1, 2], [3, 4], [5, 6]]
print('Before: ',l1)
l2=[j for i in l1 for j in i]
print('After: ',l2)

print("-----------")

#QUESTION 3
t1=(3,5,1,8,2)
t1=list(t1)
t1.sort()
print('MAX: ',t1[-1])
print('MIN: ',t1[0])

print("-------------")

#QUESTION 4
l=[(i,i**3) for i in range(1,6)]
print("LIST: ",l)