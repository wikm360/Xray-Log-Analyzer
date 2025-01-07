from base import *

print("Choose one option :")
print("1-Run Now")
print("2-Run with schedule")
option = input("Enter :")
if option == "1" :
    main("now")
elif option == "2" :
    cycle = input("Please Enter Time cycle (00:00) : ")
    main("timing" , cycle)