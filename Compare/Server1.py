#import pyodbc 
import Pyro4

#Set SA2 Connection Details
SA2_PORT = 51516
SA2_SERVER = "localhost"

#Set SA1 Serving Details
SA1_PORT = 51515

globalGrade = []
@Pyro4.expose
class honorsCheck(object):
    #Perform Database Lookup
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
                return round(course_average, 2)
            except ValueError as e:
                print(f"Value error in calculateCourseAverage: {e}")
                return None
        else:
            print("in Server1: SA1 -> Client : Error calculating average")
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

