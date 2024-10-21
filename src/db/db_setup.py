import sqlalchemy
import sqlite3
import logging
import requests
import random

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

NUM_EMPLOYEES = 5000

def create_employee_records(db_connection: sqlite3.Connection):
    """Creates an employee table with their HR related details.

    Keyword arguments:
    db_connection -- an sqlite3 database connection
    """
    cur = db_connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Employee(EmployeeId INTEGER, FirstName TEXT, LastName TEXT, Email TEXT, OfficeId TEXT, JobTitle TEXT)")

    job_titles = ["Developer", 
                  "QA", 
                  "Business Analyst", 
                  "Financial Analyst", 
                  "Project Manager", 
                  "Solutions Architect", 
                  "Controller", 
                  "Consultant"]
    
    logger.info("Getting people")
    random_person_response = requests.get(f"https://randomuser.me/api/?results={NUM_EMPLOYEES}").json()["results"]

    # First Name, last name, Employee Number, OfficeID, email
    logger.info("Making employees")
    employees = []
    for index, person in enumerate(random_person_response):
        first_name = person["name"]["first"]
        last_name = person["name"]["last"]
        email = person["email"]
        job_title = job_titles[random.randint(0, len(job_titles) - 1)]
        office_id = random.randint(0,6)
        employee = (index, first_name, last_name, email, office_id, job_title)
        employees.append(employee)
    logger.info("Inserting into db")
    cur.executemany("INSERT INTO Employee VALUES (?, ?, ?, ?, ?, ?)", employees)
    db_connection.commit()
    cur.close()

    logger.info("Done")

def create_salary_table(db_connection: sqlite3.Connection):
    """Creates an employee salary table.

    Keyword arguments:
    db_connection -- an sqlite3 database connection
    """
    cur = db_connection.cursor()
    logger.info("Creating salary table")
    cur.execute("CREATE TABLE IF NOT EXISTS Salary(EmployeeId INTEGER, EmployeeLevel TEXT, YearlyCompensation REAL)")
    salary_options = [60000, 70000, 80000, 90000, 100000, 110000]
    salaries = []
    logger.info("Creating salaries list")
    for i in range(NUM_EMPLOYEES):
        level = random.randint(0,len(salary_options) - 1)
        salary = salary_options[level]
        salaries.append((i,level,salary))
    logger.info("Inserting salaries into DB")
    cur.executemany("INSERT INTO Salary VALUES (?, ?, ?)", salaries)
    db_connection.commit()


#TODO: CREATE THIS FUNCTION
def ingest_csv_data(filename: str):
    pass

if __name__ == '__main__':
    db_connection = sqlite3.connect("utsc-exercise.db")
    create_salary_table(db_connection)

    db_connection.close()

    

        
        
         
    