#Ryan doc name: ca.py
import Pyro4

#Set SA1 Connection Details
PORT = 51515
SERVER = "localhost"



def splashScreen():
    print("-------------------------------------")
    print("     == E-Open University ==         ")
    print("   Course/unit Checking System")
    print("-------------------------------------")
    print("")


def checkStudent():
    while True:
        selection = input("Are you a current EOU Student? (y/n): ").lower()
        if selection == "y":
            return True
        elif selection == "n":
            return False

def printQualification(qual):
    print()
    print("--------your course record is as below---------------------------")
    print()
    #print(qual)
    print ("    No. | unit_title | unit_mark")
    print ("--------+------------+----------")
    i=1
    for x in qual:
        unit_title =x[0]
        unit_mark = x[1]
        print ( "   ", i, "  |   ", unit_title, "  |  ", unit_mark)
        #print (  i,  unit_title,  unit_mark)
        i +=1

def main():
    uri = "PYRO:honorsCheck@"+SERVER+":"+str(PORT)
    honors_Check=Pyro4.Proxy(uri)

    splashScreen()

    if checkStudent():
        #If The person is a student
        studentID = input("Person ID :")
        lastName = input("Last Name :")
        eouEmail = input("EOU Email Address :")
        print("Requesting Data from Server....")
        qualification = honors_Check.getQualification(studentID, lastName, eouEmail)
        print("Requesting returns from Server....")
        printQualification(qualification)

    else:
        #if the person is not a student
        print("you cannot use this system - Bye")

    
    print("")


main()
