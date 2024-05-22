import pyodbc 
import Pyro4

#Configure SQL Server Details
SQL_SERVER_NAME = "DESKTOP-5HMEDN7"
SQL_SERVER_DB = "student"

#Set Server2 Serving Details
SA2_PORT = 51516


@Pyro4.expose
class db(object):

    #Perform Database Lookup
    def __sqlQuery(self, q, arg):
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                'Server='+SQL_SERVER_NAME+';'
                                'Database='+SQL_SERVER_DB+';'
                                'Trusted_Connection=yes;')

            cursor = conn.cursor()
            cursor.execute(q, arg)
            return cursor
        except:
            return None


    #----- Exposed Methods that can be invoked
    def Authentication(self, person_id, last_name, email):
        try:
            print("in Server2: SA1 -> SA2 : Called getUserDetails")
            stu_info = list()

            print("Attempting to Perform MSSQL Database lookup")

            cursor = self.__sqlQuery('SELECT * FROM student_info WHERE person_id = ? AND last_name = ? AND email = ?', [person_id, last_name, email])
        
            if cursor is None:
                return False
            else: 
                return True
        except Exception as e:  # Proper exception handling
            print(f"An error occurred during authentication: {e}")
            return False
    
    def getUserDetails(self, person_id):
        try:
            print("in Server2: SA1 -> SA2 : Called getUserDetails")
            grades = []

            print("Attempting to Perform MSSQL Database lookup")
            cursor = self.__sqlQuery('SELECT unit_code, result_score FROM student_unit WHERE person_id = ?', [person_id])
            if cursor:
                for row in cursor:
                    # add the grades to the list
                    grades.append([row[0], row[1]])

                print("from Server2: SA2-> SA1 : Sending Grades to server 1")
                return grades
            else:
                print("No results found.")
                return None
        except:
            print("from Server2: SA2 -> SA1 : Sending Database Error")
            return None


#Accept RMI
honorsDb=db()
daemon=Pyro4.Daemon(port=SA2_PORT)                
uri=daemon.register(honorsDb, "honorsDb")


print("-----------------------------")
print(" Server2 - Interface ")
print("-----------------------------")
print()
print("Ready. Object uri =", uri)
daemon.requestLoop()

