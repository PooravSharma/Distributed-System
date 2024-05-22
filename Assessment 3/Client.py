#Ryan doc name: ca.py
import Pyro4

#Set SA1 Connection Details
PORT = 51515
SERVER = "localhost"


uri = "PYRO:honorsCheck@"+SERVER+":"+str(PORT)
server1=Pyro4.Proxy(uri)


person_Id = "";
last_Name= "";
email= "";

def splashScreen():
    print("-------------------------------------")
    print("     == E-Open University ==         ")
    print("   Course/unit Checking System")
    print("-------------------------------------")
    print("")


def checkStudent():
    while True:
        inValue = getInput("Are you a current OUST Student? (y/n): ").strip().lower()
        if inValue in ['y', 'n']:
            if inValue == "y":
                print("nice")
                return True
            elif inValue == "n":
                return False
        else:
            print("Invalid input!!! Choose 'Y' for yes or 'N' for no.")
            print("")
            
def getInput(prompt):
    editPrompt = f"{prompt}                                     (Enter 'exit' to return to start fo the application)\n"
    while True:
        user_input = input(editPrompt).strip()
        if user_input.lower() == "exit":
            print("\nReturning to start\n")
            main()
            break
        else:
            return user_input

    
def displayScore(grades):
    if grades is None:
        print("Error: No course records found.")
        return
    if not grades:
        print("No course records found.")
        return
    print()
    print("--------your course record is as below---------------------------")
    print()
    #print(qual)
    print ("    No. | unit_code | unit_mark")
    print ("--------+------------+----------")
    for i, (unit_code, unit_mark) in enumerate(grades, start=1):
        print(f"   {i:3}  |   {unit_code:<10} |  {unit_mark:<6}")

def displayAverage(course_average):
    if course_average is None:
        print("Error: Could not calculate course average.")
    else:
        print(f"Your course average is: {course_average}")

def checkDetail():
   
    if checkStudent() == True:
        # If the person is a student
        while True: 
            person_Id = getInput("What is your Student ID? ").strip()
            if person_Id:
                if not person_Id.isdigit():
                    print("\nEnter digits for Student ID\n")
                else:
                    break
            else:
                print("\n Student ID cannot be empty!!!\n")

        while True: 
            last_Name = getInput("What is your Last Name? ").strip()
            if last_Name:
                break
            else:
                print("\nLast Name cannot be empty!!!\n")
                      
        while True: 
            email = getInput("What is you OUST Email Address? ").strip()
            if email:
                break
            else:
                print("\nEmail cannot be empty!!!\n")
                
        print("Requesting Check Student Data from Client server....")
         # If the person is not a student
        if server1.checkStudent(person_Id, last_Name, email) == False:
            print("Your details does not match our records!!! Try again")
            main()
            
       
    else:
         print("Manually input your scores")

      


def menu(): 
    try:
        while True:
            print("1. Display Scores")
            print("2. Calculate Course Average")
            print("3. Calculate 8 best scores")
            print("4. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                scores = honors_check.displayScore(person_id)
                print("Requesting returns from Server....")
                displayScore(scores)
            elif choice == "2":
                course_average = honors_check.calculateCourseAverage(person_id)
                print("Requesting course average from Server....")
                displayAverage(course_average)
            elif choice == "3":
                best_8_average = honors_check.calculateBest8Average(person_id)
                print("Requesting average of best 8 scores from Server....")
                displayAverage(best_8_average)
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    except Pyro4.errors.PyroError as e:
        print("Failed to retrieve data from the server: {e}")
        print("")



    
def main():
   splashScreen()
   checkDetail()

    
if __name__ == "__main__":
    main()

