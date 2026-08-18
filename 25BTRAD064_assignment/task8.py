'''Here we are getting the user name and their age to verify that they are eligble to vote or not using a simple algorithm/simple conditional statemnet'''
y=input("Enter your name:")                                     
x=int(input("Enter the age:"))
if(x>=18):
    print("Congratulations,",y,"\nYou are Eligble to vote")
else:
    print("Sorry,",y,"\nYou are not eligble to vote")
