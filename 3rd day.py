a=input("enter a= ")
i=len(a)
for j in range(i):
    print(a)


a=int(input("Enter a= "))
if a<40:
    print("Fail")
elif a<=60 and a>40:
    print("C")
elif a<=70 and a>60:
    print("B")
elif a<=80 and a>70:
    print("B+")
elif a<=90 and a>80:
    print("A")
elif a<=100 and a>90: 
    print("A+")
else: 
    print("Invalid")