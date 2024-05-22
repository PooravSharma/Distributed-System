#import pyodbc 
import Pyro4

#Set SA2 Connection Details
SA2_PORT = 51516
SA2_SERVER = "localhost"

#Set SA1 Serving Details
SA1_PORT = 51515


globalGrade = []
globalID = ""
topAverage = ""
totalAverage = ""
@Pyro4.expose
class honorsCheck(object):

    
    #Perform Database Lookup
    def __authentication(self, person_id, last_name, email):
        try:
            print("from Server1: SA1 -> SA2 : Performing Database Request")
            # Connect to SA2 with RMI
            sa2Uri = f"PYRO:honorsDb@{SA2_SERVER}:{SA2_PORT}"
            database = Pyro4.Proxy(sa2Uri)

            # Request user details
            return database.authentication(person_id, last_name, email)
        except Exception as e:
            print("Error in __getUserDetails:", e)
            return None
    def __getUserDetails(self, person_id):
        try:
            print("from Server1: SA1 -> SA2 : Performing Database Request")
            # Connect to SA2 with RMI
            sa2Uri = f"PYRO:honorsDb@{SA2_SERVER}:{SA2_PORT}"
            database = Pyro4.Proxy(sa2Uri)

            # Request user details
            return database.getUserDetails(person_id)
        except Exception as e:
            print("Error in __getUserDetails:", e)
            return None


    # ----- Exposed Methods to be invoked by client

    # displaying individual scores
    def displayScore(self, person_id):
        globalID = person_id
        print("from server1: Client -> SA1 : Called displayScore")
        grades = self.__getUserDetails(person_id)
        globalGrade.extend(grades)
        if grades is not None:
            for unit_code, unit_score in grades:
                print(f"Unit Code: {unit_code}, Unit Score: {unit_score}")
            print("in Server1: SA1 -> Client : Sending data back to client")
            return grades
        else:
            print("in Server1: SA1 -> Client : Error retrieving data")
            return None

    # Calculating course average
    def calculateCourseAverage(self):
        print("from server1: Client -> SA1 : Called calculateCourseAverage")
        #grades = self.__getUserDetails(person_id)
        numberOfGrade = len(globalGrade)
        if globalGrade is not None:
            try:
                scores = [float(unit_score) for _, unit_score in globalGrade]
                course_average = sum(scores) / numberOfGrade if scores else 0
                print(f"in Server1: SA1 -> Client : Course average is {course_average}")
                totalAverage = round(course_average, 2)

            except ValueError as e:
                print(f"Value error in calculateCourseAverage: {e}")
                return None
        else:
            print("in Server1: SA1 -> Client : Error calculating average")
            return None

    def calculateBest8Average(self, person_id):
        grades = self.__getUserDetails(person_id)
        if grades is not None:
            try:
                # Sort grades by score in descending order
                scores = [float(unit_score) for _, unit_score in grades]
                sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
                # Select the best 8 scores
                best_8_scores = sorted_scores[:8]
                # Calculate the average of the best 8 scores
                best_8_average = sum(best_8_scores) / len(best_8_scores) if best_8_scores else 0
                print(f"in Server1: SA1 -> Client : Average of best 8 scores is {best_8_average}")
                return round(best_8_average, 2)
            except ValueError as e:
                print(f"Value error in calculateBest8Average: {e}")
                return None
        else:
            print("in Server1: SA1 -> Client : Error calculating average")
            return None

    def checkStudent(person_id, last_name, email):
        try:
            print("from Server1: SA1 -> SA2 : Performing Database Request")
            # Connect to SA2 with RMI
            sa2Uri = f"PYRO:honorsDb@{SA2_SERVER}:{SA2_PORT}"
            server2 = Pyro4.Proxy(sa2Uri)

            # Request user details
            return server2.authentication(person_id, last_name, email)
        except Exception as e:
            print("Error in __getUserDetails:", e)
            return None
        
    def gettopAverage(self):
        globalGrade = sorted(globalGrade, key = lambda x: [1], reverse = True)
        topGrades = globalGrade[:8]
        totalSum = sum(grade for _, grade in topGrades)
        topAverage = totalSum/8

        

    def honoursEvalutaion(self):
        self.gettopAverage()
        self.calculateCourseAverage()
        passedGrade = len(globalGrade)
        failNumber= sum(1 for grade in globalGrade if grade < 50)

        if passedGrade <= 15:
            return f"{globalID}, {totalAverage}, completed less than 16 units! DOES NOT QUALIFY FOR HONORS STUDY!"
    
        if failNumber >= 6:
            return f"{globalID}, {totalAverage}, with 6 or more Fails! DOES NOT QUALIFY FOR HONORS STUDY!"
    
        if totalAverage >= 70:
            return f"{globalID}, {totalAverage}, QUALIFIES FOR HONOURS STUDY!"
    
        elif 65 <= totalAverage < 70 and topAverage >= 80:
            return f"{globalID}, {totalAverage}, {topAverage}, QUALIFIES FOR HONOURS STUDY!"
    
        elif 65 <= totalAverage < 70 and topAverage < 80:
            return f"{globalID}, {totalAverage}, {topAverage}, MAY HAVE GOOD CHANCE! Need further assessment!"
    
        elif 60 <= totalAverage < 65 and topAverage >= 80:
            return f"{globalID}, {totalAverage}, {topAverage}, MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator’s permission!"
    
        else:
            return f"{globalID}, {totalAverage}, DOES NOT QUALIFY FOR HONORS STUDY!"


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
