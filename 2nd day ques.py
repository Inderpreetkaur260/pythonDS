#QUESTION 1
print("--------------------------")
name=input('NAME= ')
std=int(input('CLASS= '))
section=input('SECTION= ')
print('STUDENT MARKS')
sub1=int(input('MATHS= '))
sub2=int(input('ENGLISH= '))
sub3=int(input('SCIENCE= '))
sub4=int(input('PUNJABI= '))
sub5=int(input('SOCIAL SCIENCE= '))
grandtotal=sub1+sub2+sub3+sub4+sub5
average= grandtotal/5
print('Name-  ',name)
print('Class-  ',std)
print('Section-  ',section)
print('Total- ',grandtotal)
print('Percentage-  ',average)


#QUESTION 2
print("--------------------------")
a=int(input('ENTER a= '))
b=int(input('ENTER b= '))
c=int(input('ENTER c= '))
sum=a+b+c
print('Value of a= ',a)
print('Value of b= ',b)
print('Value of c= ',c)
print('SUM OF THREE NUMBERS:- ',sum)


#QUESTION 3
print("--------------------------")
a=int(input('Enter a= '))
square=a*a
print('Square of a= ',square)


#QUESTION 4
print("--------------------------")
a=input('Temperature in celcius = ')
a=float(a)
b=(a*(9/5))+32
print('Temp in cel= ', a)
print('Temp in fah= ',b)


#QUESTION  5
print("--------------------------")
i=int(input('Enter i= '))
j=int(input('Enter j= '))
quotient=i//j
remainder=i%j
print('QUOTIENT= ',quotient)
print('REMAINDER= ',remainder)