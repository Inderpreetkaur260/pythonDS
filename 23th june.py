#QUESTION 1
print("-------CODERAIL TICKRT BOOKING SYSTEM-------")

name=input("Enter passanger name:- ")
age=int(input("Enter age:- "))

print("Choose your travel class:")
print("1. FIRST CLASS: ₹1500")
print("2. SECOND CLASS: ₹1000")
print("3. SLEEPER CLASS: ₹500")
class_choice=input("Choose from the above mentioned options:- ")
if class_choice=="1":
    class_price=1500
elif class_choice=="2":
    class_price=1000
elif class_choice=="3":
    class_price=500
else:
    print("Invalid choice")
    exit()

if age < 5:
    print("Free ticket for children under 5")
elif age >= 60:
    print("20% discount is applied")
    total_price = class_price * 0.8  
else:
    total_price = class_price

print("MEAL OPTION")
meal_choice = input("Do you want to add a meal for ₹200? (yes/no): ")
if meal_choice == 'yes':
    total_price += 200
else:
    print("No meal added")

print("----Ticket Summary----")
print("Passenger name: ",name)
print("Passenger age: ",age)
print("Travel class: ",class_choice)
print("Meal Added: ",meal_choice)
print("Total price: ",total_price) 

print("------------------------")

#QUESTION 2
print("-------WELCOME TO BURGER KING-------")

print("Menu:\n")
print("1 Whopper Burger - ₹150")
print("2 Crispy Veg     - ₹100")
print("3. Chicken Wings  - ₹120")

a = input("Enter the item number: ")

if a == "1":
    price = 150
elif a == "2":
    price = 100
elif a == "3":
    price = 120
else:
    print("Invalid choice. Please restart the program and choose a valid item.")
    exit()
q=int(input("Enter the quantity: "))

total_price = price * q
print("Total price: ",total_price)  

dis = "No discount"
coupon_code=input("Do you have a coupon code? (yes/no): ")
if coupon_code == 'yes':
    coupon_code = input("Enter the coupon code: ")
    if coupon_code == "KING50":
        dis= "50% off"
        dprice = total_price-(total_price * 0.5)
    elif coupon_code == "BK20":
        dis = "Rs. 20 off"
        dprice = total_price - 20
    else:
        print("Invalid coupon code. No discount applied.")
elif coupon_code == 'no':
    dprice = total_price
else:
    print("Invalid choice for coupon code. Please restart the program and choose 'yes' or 'no'.")
    exit()

print("-----------------------------------------")
print("Order Summary: ")
print("Item: ", a)
print("Quantity: ", q)
print("Original Price: Rs.", total_price)
print("Discount: ", dis)
print("Final Price after discount: Rs.", dprice)
print("Thank you for ordering!!!!")



