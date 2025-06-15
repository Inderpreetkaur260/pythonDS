#Question 1
str1=input("enter a string= ")
n=len(str1)
if n<2:
    print("Invalid")
else:
    str2=str1[:2]
    str3=str1[n-2:n]
    str4=str2+str3
    print(str4)
 
print("--------------")

#QUESTION 2
str1=input("Enter first string= ")
str2=input("Enter second string= ")
a=str1[:1]
b=str2[:1]
str1=str1.replace(a,b)
str2=str2.replace(b,a)
print("New String= ",str1," ",str2)

print("--------------")

#QUESTION 3
str1=input("Enter a string: ")
n=len(str1)
if n<3:
    print("String- ",str1)
elif str1.endswith("ing"):
    print("New String- ",str1+"ly")
else:
    print("New String- ",str1+"ing")

print("--------------")


#QUESTION 4
str1=input("Enter a String: ")
if len(str1)==0:
    print("String is empty")
else:
    a=int(input("Enter the index: "))
    print("String= ",str1)
    print("New String= ",str1[:a]+str1[a+1:])

