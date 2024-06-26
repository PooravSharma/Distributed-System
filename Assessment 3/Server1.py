#import pyodbc 
import Pyro4

#Set SA2 Connection Details
SA2_PORT = 51516
SA2_SERVER = "localhost"

#Set SA1 Serving Details
SA1_PORT = 51515


globalGrade = []
globalID = ""
topAverage = 0.0
totalAverage = 0.0


@Pyro4.expose
class honorsCheck(object):

    
    #Perform Database Lookup
    def getUserDetails(self, person_id, last_name, email):
        global globalGrade
        global globalID
        globalID = person_id
        try:
            print("from Server1: SA1 -> SA2 : Performing Database Request")
            # Connect to SA2 with RMI
            sa2Uri = f"PYRO:honorsDb@{SA2_SERVER}:{SA2_PORT}"
            database = Pyro4.Proxy(sa2Uri)
            grades = database.getUserDetails(person_id, last_name, email)
            if grades is not None:
                globalGrade = [(unit_code, float(unit_score)) for unit_code, unit_score in grades]
                return grades
                # Request user details
            #return database.getUserDetails(person_id, last_name, email)
            return grades
        except Exception as e:
            print("Error in getUserDetails:", e)
            return None

    # ----- Exposed Methods to be invoked by client

    # Calculating course average
    def calculateCourseAverage(self):
        global totalAverage
        numberOfGrade = len(globalGrade)
        if globalGrade is not None:
            try:
                scores = [float(unit_score) for _, unit_score in globalGrade]
                course_average = sum(scores) / numberOfGrade if scores else 0
              
                totalAverage = round(course_average, 2)

            except ValueError as e:
                print(f"Value error in calculateCourseAverage: {e}")
                return None
        else:
            print("in Server1: SA1 -> Client : Error calculating average")
            return None
        
    def gettopAverage(self):
        global globalGrade
        global topAverage
        globalGrade = sorted(globalGrade, key = lambda x: [1], reverse = True)
        topGrades = globalGrade[:8]
        totalSum = sum(grade for _, grade in topGrades)
        topAverage = totalSum / len(topGrades)
        topAverage = round(topAverage, 2)

    def manualHonours(self, manualList: list):
        global globalGrade
        globalGrade = manualList
        global globalID
        globalID = "User"
        return self.honoursEvaluation()

    def honoursEvaluation(self):
        global globalGrade
        global globalID
        self.gettopAverage()
        self.calculateCourseAverage()
        passedGrade = len(globalGrade)
        failNumber= sum(1 for _, grade in globalGrade if grade < 50) 
        print("in Server1: SA1 -> Client : Evaluation Result")
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
