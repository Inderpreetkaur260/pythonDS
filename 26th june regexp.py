import regex
pass1='(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_!@#$%^&*]).{8,}'
b=input("Enter your password:- ")
ans=regex.match(pattern=pass1,string=b)
if ans:
    print("Valid")
else:
    print("Invalid")


patt='[a-zA-Z0-9._]+@[a-zA-Z0-9]+.[a-z]{2,6}'
str1='my mail id is indersaini_123@gmail.com and other id is saininder.765@gmail.in and one more id is saini564_inder@gmail.com'
ans=regex.findall(pattern=patt,string=str1)
print(ans)
a=input("Enter your email:- ")
ans=regex.findall(pattern=patt,string=a)
if not ans:
    print("Match not found")
else:
    print(ans)