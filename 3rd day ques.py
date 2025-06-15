
#QUESTION 1
a=int(input("Enter a= "))
if a==1:
    print("JAN")
elif a==2:
    print("FEB")
elif a==3: 
    print("MAR")
elif a==4:
    print("APR")
elif a==5:
    print("MAY")
elif a==6:
    print("JUN")
elif a==7: 
    print("JLY")
elif a==8: 
    print("AUG")
elif a==9:
    print("SEP")
elif a==10:
    print("OCT")
elif a==11:
    print("NOV")
elif a==12:
    print("DEC")
else:
    print("INVALID MONTH")

print("********************************************")
#QUESTION 2
a=int(input("Enter a= "))
b=int(input("Enter b= "))
firstname=input("enter first name= ")
lastname=input("Enter last name= ")

if a>b:
    print("a is greater than b")
elif a==b:
    print("a is equal to b")
else:
    print("b is greater than a")

if a>b:
    for i in range (5):
        print(firstname)
elif a==b:
    print("NULL")
else:
    for i in range(3):
        print(lastname)

print("********************************************")
#QUESTION 3
str1=input("Enter str1= ")
str2=input("Enter str2= ")

if str1 is str2:
    print("str1 is equal to str2")

if str1==str2:
    print("str1 is equal to str2")
else: 
    print("Not equal")

print("********************************************")
#QUESTION 4
string1=input("Enter string1= ")
string2=input("Enter string2= ")

if string1 is string2:
    print("string1 is equal to string1")
else: 
    print("string1 is not equal to string2")

print("********************************************")
#QUESTION 5
a = int(input("Enter a : "))
sum= 0
for i in range(0,a+1):
   sum=sum+i
print("Sum = ",sum)

print("********************************************")
#QUESTION 6
a=int(input("Enter a= "))
print("Even numbers are= ")
for i in range(0,a+1):
    if i%2==0:
        print(i, end=" ")
print()   
print("********************************************")
#QUESTION 7
a=int(input("Enter a= "))
option=input("Enter your choice '+' or '-' = ")

if option== "+" :
    for i in range(a):
        print(i, end=" ")
elif option== "-":
    for i in range(a,-1,-1):
        print(i, end=" ")
else:
    print("Invalid")

print("********************************************")
#QUESTION 8
a=int(input("Enter a= "))
print("Table of a= ")
for i in range(1,11):
    print(a,"x",i,"=",a*i)

print("********************************************")
#QUESTION 9
for i in range(1,5):
    for j in range(1,i+1):
        print(j, end=" ")
    print()    

print("********************************************")
#QUESTION 10
a = int(input("Enter a= "))
print("Squares of {a} natural numbers= ")
for i in range(1,a + 1):
    print(i*i)

