# Ryan doc name: ca.py
import Pyro4

# Set SA1 Connection Details
PORT = 51515
SERVER = "localhost"

uri = "PYRO:honorsCheck@" + SERVER + ":" + str(PORT)
honors_Check = Pyro4.Proxy(uri)

person_id = ""
last_name = ""
email = ""
manualScore = []

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


def userInput(prompt):
    editPrompt = f"{prompt}                                     (Enter 'done' when Finish or 'exit' to Restart)\n"
    while True:
        user_input = input(editPrompt).strip()
        if user_input.lower() == "done":
            print("\nEvaluating the honors qualification\n")
            checkingHonors()
            break
        elif user_input.lower() == "exit":
            print("\nReturning to start\n")
            break
        else:
            return user_input


def displayScore(grades):
    if grades is None:
        print("Authentication failed!")
        return
    if not grades:
        print("No course records found.")
        return
    print()
    print("--------your course record is as below---------------------------")
    print()
    # print(qual)
    print("    No. | unit_code | unit_mark")
    print("--------+------------+----------")
    for i, (unit_code, unit_mark) in enumerate(grades, start=1):
        print(f"   {i:3}  |   {unit_code:<10} |  {unit_mark:<6}")


def displayAverage(course_average):
    if course_average is None:
        print("Error: Could not calculate course average.")
    else:
        print(f"Your course average is: {course_average}")


def checkDetail():
    global person_id
    global last_name
    global email

    if checkStudent() == True:
        # If the person is a student
        while True:
            person_id = getInput("What is your Student ID? ").strip()
            if person_id:
                if not person_id.isdigit():
                    print("\nEnter digits for Student ID\n")
                else:
                    break
            else:
                print("\n Student ID cannot be empty!!!\n")

        while True:
            last_name = getInput("What is your Last Name? ").strip()
            if last_name:
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

        scores = honors_Check.getUserDetails(person_id, last_name, email)

        displayScore(scores)
        if scores is not None:
            course_average = honors_Check.honoursEvaluation()
            print("Requesting course average from Server....")
            displayAverage(course_average)

        else:
            print("")
            print("Try again")
            main()
    else:
        print("Manually input your scores")
        manualInput()


def manualInput():
    global manualScore
    unit_scores = {}
    failures = {}

    manualScore.clear()
    while len(unit_scores) < 16 or len(unit_scores) > 30:
        while True:
            unitname = userInput("Enter the unit name: ")
            if unitname:
                break
            else:
                print("\nUnit name cannot be empty!!!\n")

        while True:
            score = userInput("Enter the score (0.00 to 100.00): ")
            if score:
                try:
                    score = float(score)
                    if 0.00 <= score <= 100.00:
                        break
                    else:
                        print("Invalid score. Please enter a score between 0.00 and 100.00.")

                except ValueError:
                    print("\nEnter a valid number for the score\n")
            else:
                print("\nScore cannot be empty!!!\n")
        # Check score validity


        # Initialize unit in dictionary if it does not exist
        if unitname not in unit_scores:
            unit_scores[unitname] = []
            failures[unitname] = 0

        # Check for failure count and repetition rules
        if failures[unitname] >= 2:
            print(f"The unit {unitname} cannot fail more than twice.")
            print("You fail your course")
            main()
        if len(unit_scores[unitname]) >= 3:
            print(f"The unit {unitname} cannot be entered more than 3 times.")
            continue

        if score >= 50 and unit_scores[unitname]:
            print(f"The unit {unitname} cannot repeat if it has a score 50 or above.")
            continue
        # Add score and update failure count
        unit_scores[unitname].append(score)
        if score < 50:
            failures[unitname] += 1
        manualScore.append((unitname, score))
    # Print the final scores
    #for unit, scores in unit_scores.items():
        #print(f"Unit: {unit}, Scores: {scores}")



def checkingHonors():
    global manualScore
    displayScore(manualScore)
    uri = "PYRO:honorsCheck@" + SERVER + ":" + str(PORT)
    honors_Check = Pyro4.Proxy(uri)
    honors_Check.manualHonors(manualScore)


def menu():
    global person_id
    uri = "PYRO:honorsCheck@" + SERVER + ":" + str(PORT)
    honors_Check = Pyro4.Proxy(uri)
    try:
        while True:
            print("1. Display Scores")
            print("2. Calculate Course Average")
            print("3. Calculate 8 best scores")
            print("4. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                scores = honors_Check.displayScore(person_id, last_name, email)
                print("Requesting returns from Server....")
                displayScore(scores)
            elif choice == "2":
                course_average = honors_Check.honoursEvaluation()
                print("Requesting course average from Server....")
                displayAverage(course_average)
            elif choice == "3":
                best_8_average = honors_Check.calculateBest8Average(person_id)
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
