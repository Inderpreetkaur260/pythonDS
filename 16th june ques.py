#QUESTION 1
l=[23,56,76,9,34,67,25,98,12,34]
print(l)

print("------------")

#QUESTION 2
l1=[1,10,100,3,6,8]
l1.insert(3,59)
l1.append(5)
print(l1)
print(len(l1))

print("-------------")

#QUESTION 3
l2=[3,'inder',7,5,8,10,'saini,35']
print(l2[::2])

print("-------------")

#QUESTION 4
l3=["Gaurav",12,23,33.33,"Sharma",True]
for i in l3:
    if type(i)==str:
        print(i)

print("-------------")

#QUESTION 5
l4=[23,65,75,89,45,90,30,80]
sum=0
for i in l4:
    sum+=i
print(sum)

print("-----------")

#QUESTION 6
l5=['inder','hargun','maninder','komal','dilrose']
str1=input("Enter another friend= ")
l5.append(str1)
print(l5)
str2=input("Most important friend= ")
n=int(input("Enter index= "))
l5.insert(n,str2)
print(l5)
    