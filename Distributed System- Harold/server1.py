#import pyodbc 
import Pyro4

#Set SA2 Connection Details
SA2_PORT = 51516
SA2_SERVER = "localhost"

#Set SA1 Serving Details
SA1_PORT = 51515


@Pyro4.expose
class honorsCheck(object):
    #Perform Database Lookup
    def getUserDetails(self, person_id, last_name, email):
        try:
            print("from Server1: SA1 -> SA2 : Performing Database Request")
            # Connect to SA2 with RMI
            sa2Uri = f"PYRO:honorsDb@{SA2_SERVER}:{SA2_PORT}"
            database = Pyro4.Proxy(sa2Uri)

            # Request user details
            return database.getUserDetails(person_id, last_name, email)
        except Exception as e:
            print("Error in getUserDetails:", e)
            return None


    # ----- Exposed Methods to be invoked by client

    # displaying individual scores
    def displayScore(self, person_id, last_name, email):
        print("from server1: Client -> SA1 : Called displayScore")
        grades = self.getUserDetails(person_id, last_name, email)
        if grades is not None:
            for unit_code, unit_score in grades:
                print(f"Unit Code: {unit_code}, Unit Score: {unit_score}")
            print("in Server1: SA1 -> Client : Sending data back to client")
            return grades
        else:
            print("in Server1: SA1 -> Client : Error retrieving data")
            return None

    # Calculating course average
    def calculateCourseAverage(self, person_id, last_name, email):
        print("from server1: Client -> SA1 : Called calculateCourseAverage")
        grades = self.getUserDetails(person_id, last_name, email)
        if grades is not None:
            try:
                scores = [float(unit_score) for _, unit_score in grades]
                course_average = sum(scores) / len(scores) if scores else 0
                print(f"in Server1: SA1 -> Client : Course average is {course_average}")
                return round(course_average, 2)
            except ValueError as e:
                print(f"Value error in calculateCourseAverage: {e}")
                return None
        else:
            print("in Server1: SA1 -> Client : Error calculating average")
            return None

    def calculateBest8Average(self, person_id, last_name, email):
        print("from server1: Client -> SA1 : Called calculateCourseAverage")
        grades = self.getUserDetails(person_id, last_name, email)
        if grades is not None:
            try:
                scores = [float(unit_score) for _, unit_score in grades]
                sorted_scores = sorted(scores, reverse=True)
                # Select the best 8 scores
                best_8_scores = sorted_scores[:8]
                # Calculate the average of the best 8 scores
                best_8_average = sum(best_8_scores) / len(best_8_scores)
                print(f"in Server1: SA1 -> Client : Average of best 8 scores is {best_8_average}")
                return round(best_8_average, 2)
            except ValueError as e:
                print(f"Value error in calculateBest8Average: {e}")
                return None

        else:
            print("in Server1: SA1 -> Client : Error calculating average")
            return None

    def honoursEvaluation(self, person_id, last_name, email):
        print("from server1: Client -> SA1 : Called honoursEvaluation")
        grades = self.getUserDetails(person_id, last_name, email)
        if grades is not None:
            grade = [float(unit_score) for _, unit_score in grades]
            passedGrade = len(grade)
            failNumber = sum(1 for result_score in grade if result_score < 50)

            totalAverage = self.calculateCourseAverage(person_id, last_name, email)
            topAverage = self.calculateBest8Average(person_id, last_name, email)

            if passedGrade <= 15:
                return f"{person_id}, {totalAverage}, completed less than 16 units! DOES NOT QUALIFY FOR HONORS STUDY!"

            if failNumber >= 6:
                return f"{person_id}, {totalAverage}, with 6 or more Fails! DOES NOT QUALIFY FOR HONORS STUDY!"

            if totalAverage >= 70:
                return f"{person_id}, {totalAverage}, QUALIFIES FOR HONOURS STUDY!"

            elif 65 <= totalAverage < 70 and topAverage >= 80:
                return f"{person_id}, {totalAverage}, {topAverage}, QUALIFIES FOR HONOURS STUDY!"

            elif 65 <= totalAverage < 70 and topAverage < 80:
                return f"{person_id}, {totalAverage}, {topAverage}, MAY HAVE GOOD CHANCE! Need further assessment!"

            elif 60 <= totalAverage < 65 and topAverage >= 80:
                return f"{person_id}, {totalAverage}, {topAverage}, MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator’s permission!"

            else:
                return f"{person_id}, {totalAverage}, DOES NOT QUALIFY FOR HONORS STUDY!"
        else:
            print("in Server1: SA1 -> Client : Error retrieving data")
            return None
    #Accept RMI
honors_Check=honorsCheck()
daemon=Pyro4.Daemon(port = SA1_PORT)                
uri=daemon.register(honors_Check, "honorsCheck")

print("--------------------")
print(" Server 1: Interface")
print("--------------------")
print()
print("Ready. Object uri =", uri)
daemon.requestLoop()

