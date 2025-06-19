# Question 1
a=int(input("Enter the number of items: "))
dict={}
for i in range(a):
    key=input("Enter the key: ")
    value=input("Enter the value: ")
    dict[key]=value
print("Dictionary: ",dict)

print("-----------------")

#QUESTION 2
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

# #QUESTION 3
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

#QUESTION 4
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

#QUESTION 5
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

#QUESTION 6
li=[20,30,40,[57,66,30,[70,80],"Hello"],50,True]
print(li)
li[3][3].insert(1,76)
li[3].insert(1,88)
print(li)

print("--------------")

#QUESTION 7
print("-----WELCOME TO TRIP PLANNER-----")

budget = int(input("Enter your budget (5000-10000, 10000-20000, 20000-30000, 30000-40000): "))

if 5000 <= budget <= 10000:
    countries = {"Nepal": "Pashupatinath Temple", "Bhutan": "Tiger's Nest"}
elif 10001 <= budget <= 20000:
    countries = {"Thailand": "Phuket", "Vietnam": "Ha Long Bay"}
elif 20001 <= budget <= 30000:
    countries = {"India": "Taj Mahal", "Australia": "Sydney Opera House", "USA": "Statue of Liberty"}
elif 30001 <= budget <= 40000:
    countries = {"France": "Eiffel Tower", "Japan": "Mount Fuji", "Canada": "Niagara Falls"}
else:
    print("Invalid budget")
    countries = {}

if countries:
    print("Countries available under your budget are:")
    for i in countries:
        print(i)

    choice = input("Select your choice: ")

    if choice in countries:
        print("The place to visit in", choice, "is", countries[choice])
    else:
        print("Invalid choice")
