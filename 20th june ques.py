#QUESTION 1
for i in range(1,51):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

print("--------------------------")

# #QUESTION 2
print("Prime numbers from 1 to 100")
for n in range(1,101):
    if n> 1:
        for i in range(2, n):
            if n % i == 0:
                break
        else:
            print(n)

print("-------------------") 

#QUESTION 3
a=int(input("Enter a= "))
if a<60:
    print("F")
elif a<=69 and a>60:
    print("D")
elif a<=79 and a>70:
    print("c")
elif a<=89 and a>80:
    print("B")
elif a<=100 and a>90: 
    print("A")
else: 
    print("Invalid")

print("------------------")

#QUESTION 4
a=int(input("Enter a= "))
print("Table of a= ")
for i in range(1,11):
    print(a,"x",i,"=",a*i)

print("-----------------")

#QUESTION 5
li=[]
for i in range(1,21):
    if i%2==0:
        li.append(i**2)
print(li)

print("----------------")

#QUESTION 6
year=int(input("Enter a year: "))
if year%4==0:
    if year%100==0:
        if year%400==0:
            print(year,"is a leap year")
        else:
            print(year,"is not a leap year")
    else:
        print(year,' is a leap year')
else:
    print(year,' is not a leap year')

print("-------------")

#QUESTION 7
a1=float(input("Enter side 1st of triangle: "))
a2=float(input("Enter side 2nd of triangle: "))
a3=float(input("Enter side 3rd of triangle: "))
if a1+a3>a2 or a1+a2>a3 or a2+a3>a1:
    if a1==a2==a3:
        print("Equilateral triangle")
    elif a1==a2 or a2==a3 or a3==a1:
        print("Isosceles triangle")
    elif a1**2==a2**2 + a3**2 or a2**2==a1**2 + a3**2 or a3**2==a1**2 + a2**2:
        print("Right angled triangle")
    else:
        print("Scalene triangle")
else:
    print("Not a triangle")

print("--------------")

#question 8 
a=int(input("Enter a number: "))
if a>0:
    print("It is a positive number")
elif a<0:
    print("It is a negative number")
else:
    print("It is a zero")


#QUESTION 9
password = input("Enter your password: ")
has_upper = False
has_lower = False
has_digit = False
has_special = False
special_chars = "!@#$%^&*()_+-={}[]|:;<>,.?/"

if len(password) >= 8:
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_chars:
            has_special = True

    if has_upper and has_lower and has_digit and has_special:
        print(" Password is strong!")
    else:
        print(" Password is weak. Make sure it has:")
        if not has_upper:
            print("- At least one uppercase letter")
        if not has_lower:
            print("- At least one lowercase letter")
        if not has_digit:
            print("- At least one digit")
        if not has_special:
            print("- At least one special character")
else:
    print(" Password too short! Must be at least 8 characters.")

print("-------------")

#QUESTION 10
def bmi(weight, height):
    bmi_value = weight / (height ** 2)
    if bmi_value < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_value < 24.9:
        return "Normal weight"
    elif 25 <= bmi_value < 29.9:
        return "Overweight"
    else:
        return "Obesity"

weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in meters: "))
print("BMI category is:", bmi(weight, height))

print("-----------------")

#QUESTION 11
day=int(input("Enter the number for day: "))
if day==1:
    print("Monday")
elif day==2:
    print("Tuesday")
elif day==3:
    print("Wednesday")
elif day==4:
    print("Thursday")
elif day==5:
    print("Friday")
elif day==6:
    print("Saturday")
elif day==7:
    print("Sunday")
else:
    print("Invalid day")

print("------------------")

#QUESTION 12
price = float(input("Enter the price of the product: "))
if price>1000:
        discount= 0.1
elif price>500 and price<1000:
        discount = 0.05
elif price<500:
        discount=0
discount_price = price - (price * discount)
print("The original price is: ", price)
print("The discounted price is: ",discount_price)

print("--------------")

#QUESTION 13
a=int(input("Enter a number: "))
sum=0
for i in range(1,a+1):
    sum+=i
print("Sum of 1st ",a," natural numbers is: ",sum)

print("-----------------")

#QUESTION 14
employee__details={2301210:{'NAME':'DAMON','DEPARTMENT':'ACCOUNTS','SALARY':50000},
      2301211:{'NAME':'STEPHEN','DEPARTMENT':'TECHNOLOGY','SALARY':60000},
      2301212:{'NAME':'CAROLINE','DEPARTMENT':'TRANSPORT','SALARY':40000},
      2301213:{'NAME':'ELENA','DEPARTMENT':'MEDICAL','SALARY':45000},
      2301214:{'NAME':'BONNI','DEPARTMENT':'HR','SALARY':70000}}
list=[]
for i in employee__details:
    if employee__details[i]['SALARY']>50000:
        list.append(employee__details[i]['NAME'])
        print("Employees with salary greater than 50000: ",list)

print("-----------------")

#QUESTION 15
s=input("Enter a string: ")
count=0
for i in s:
    if i=='a'or i=='A' or i=='e' or i=='E' or i=='i' or i=='I' or i=='o' or i=='O' or i=='u' or i=='U':
        count+=1
print("Number of vowels in the given string= ",count)

print("--------------------")

#QUESTION 16
a=int(input("Enter a number: "))
sum=0
while a>0:
    a1=a%10
    a=a//10
    sum+=a1
print("Sum of digits of the given number is: ",sum)

print("--------------")

#QUESTION 17
n=int(input("Enter n: "))
for i in range(n+1):
    for j in range(i):
        print("*",end="")
    print()

print("--------------")

#QUESTION 18
import random
ans=random.randint(1,100)
guess =int(input("guess the number: "))

while(guess!=ans):
    if guess<ans:
        print("guess is too low")
    else:
        print("guess is too high")
    guess=int(input("guess the number: "))

print("You made a correct Guess")

print("--------------")

#QUESTION 19
n=int(input("Enter a number: "))
print("Even numbers upto ",n," :")
for i in range(1,n+1):
    if i%2==0:
        print(i,end=" ")

print("----------------")

#QUESTION 20
li=[3,24,25,67,34,25,98,6,25,90,25,87,65]
for i in li:
    if i==25:
        ele=True
        break
    else:
        ele=False
if ele:
    print("25 is present in the list")
else:
    print("25 is not present in the list")

l=len(li)
print("Length of the list is ",l)

count=0
for i in li:
    if i==25:
        count+=1
print("Total occurence of 25 is ",count)

print("Traversing elements of list........")
for i in li:
    print(i,end=" ")
print()
print("Even numbers in the list......")
for i in li:
    if i%2==0:
        print(i,end=" ")

print("------------------")

#QUESTION 21
s=input("Enter a string: ")
print(s)
print(len(s))
s=s[::-1]
if str == s:
    print("The string is a palindrome.")
else:
    print("The string is not a palindrome.")
print(s[len(s)//2])
print(s[-2])

print("----------------")

#QUESTION 22
print("Welcome to Calci")
print("1.Power 2.Sum 3.Sub 4.Multiple")
choice=int(input("Enter your choice: "))
if choice==1:
    num1=float(input("Enter 1st number for power: "))
    num2=float(input("Enter 2nd number for power: "))
    print("Result of power is: ",num1**num2)
elif choice==2:
    num1=float(input("Enter 1st number for sum: "))
    num2=float(input("Enter 2nd number for sum: "))
    print("Result of sum is: ",num1+num2)
elif choice==3:
    num1=float(input("Enter 1st number for sub: "))
    num2=float(input("Enter 2nd number for sub: "))
    print("Result of sub is: ",num1-num2)
elif choice==4:
    num1=float(input("Enter 1st number for multiple: "))
    num2=float(input("Enter 2nd number for multiple: "))
    print("Result of multiple is: ",num1*num2)
else:
    print("Wrong choice")

print("-------------------")

#QUESTION 23
li= ['abc', 'xyz', 'aba', '1221']
count=0
for i in li:
    if len(i)>=2 and i[0]==i[-1]:
        count+=1
print("Count= ",count)