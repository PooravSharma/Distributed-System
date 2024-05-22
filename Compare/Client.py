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
        selection = input("Are you a current OUST Student? (y/n): ").lower()
        if selection == "y":
            return True
        elif selection == "n":
            return False

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
def main():
    uri = "PYRO:honorsCheck@"+SERVER+":"+str(PORT)
    honors_check=Pyro4.Proxy(uri)

    splashScreen()

    if checkStudent():
        # If the person is a student
        person_id = input("Person ID: ").strip()
        last_name = input("Last Name: ").strip()
        email = input("OUST Email Address: ").strip()

        if not person_id or not last_name or not email:
            print("All fields are required.")
            return

        print("Requesting Data from Server....")
        try:
            while True:
                print("1. Display Scores")
                print("2. Calculate Course Average")
                print("3. Exit")
                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    scores = honors_check.displayScore(person_id)
                    print("Requesting returns from Server....")
                    displayScore(scores)
                elif choice == "2":
                    course_average = honors_check.calculateCourseAverage()
                    print("Requesting course average from Server....")
                    displayAverage(course_average)
                elif choice == "3":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
        except Pyro4.errors.PyroError as e:
            print(f"Failed to retrieve data from the server: {e}")
    else:
        # If the person is not a student
        print("You cannot use this system - Bye")

    print("")
if __name__ == "__main__":
    main()
