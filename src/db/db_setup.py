import sqlalchemy
import sqlite3
import logging
import requests
import random
import pandas as pd
import shutil


"""




THIS WAS USED FOR SETUP, IGNORE THIS





"""

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

def create_employee_records_csv():
    """Creates an employee table with their HR related details.
    """
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
        employee = (index + NUM_EMPLOYEES, first_name, last_name, email, office_id, job_title)
        employees.append(employee)
    
    columns = ["EmployeeId", "FirstName", "LastName", "Email", "OfficeId", "JobTitle"]

    logger.info("Creating dataframe")
    df = pd.DataFrame(employees, columns=columns, index=None)
    logger.info("Writing to csv")
    df.to_csv("legacy_employees.csv")
    logger.info("Done")

def create_salary_table(db_connection: sqlite3.Connection):
    """Creates an employee salary table.

    Keyword arguments:
    db_connection -- an sqlite3 database connection.
    """
    cur = db_connection.cursor()
    logger.info("Creating salary table")
    cur.execute("CREATE TABLE IF NOT EXISTS Salary(EmployeeId INTEGER, EmployeeLevel TEXT, YearlyCompensation REAL)")
    salary_options = [60000, 70000, 80000, 90000, 100000, 110000]
    salaries = []
    logger.info("Creating salaries list")
    for i in range(NUM_EMPLOYEES, NUM_EMPLOYEES + NUM_EMPLOYEES):
        level = random.randint(0,len(salary_options) - 1)
        salary = salary_options[level]
        salaries.append((i,level,salary))
    logger.info("Inserting salaries into DB")
    cur.executemany("INSERT INTO Salary VALUES (?, ?, ?)", salaries)
    db_connection.commit()


"""


YOUR TASK STARTS HERE


"""

def connect_to_db(db_path: str):
    """Connects to an sqlite3 database.
    
    Keyword arguments:
    db_path -- the path where the .db file lives. If you are working in the db directory already, just type in the db
    name (e.g. utsc-exercise.db).

    Returns: an sqlalchemy engine (this will suffice for a connection).
    """
    return sqlalchemy.create_engine(f"sqlite:///{db_path}")

def insert_employee_data_into_db(db_connection: sqlalchemy.Engine, df: pd.DataFrame):
    """Inserts employee data into an sqlite3 database.
    
    Keyword arguments:
    db_connection: an sqlalchemy engine.
    df: the dataframe that you want to insert into the database.
    """
    df.to_sql("Employee", con=db_connection, if_exists="append", index=False)


#New function to remove the employees that were added to the table
def remove_added_employees_from_db():
    "Removes employees that were added from the CSV"
    db_connection = sqlite3.connect('utsc-exercise.db')
    cur = db_connection.cursor()
    logger.info("Deleting employee IDs 5000 and above")
    cur.execute("DELETE FROM EMPLOYEE WHERE EMPLOYEEID >= 5000")
    logger.info("Deleted")
    db_connection.commit()
    db_connection.close()

#New function to return the number of records in the employee table
def get_count_of_records_in_employee_table():
    """Returns the count of records in the employees table
    """
    engine = connect_to_db('utsc-exercise.db')
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM Employee"))
        count = result.scalar()  # This will give you the count as an integer
        print(f'There are {count} records in the Employee Table')
        return count
    

def remove_unnamed_columns(df):
    """Removes the column that contains the word 'Unnamed' from a dataframe.

    
    Keyword arguments:
    df: a dataframe that you want to remove an 'Unnamed' column from.

    Returns: a cleaned dataframe without the 'Unnamed' column.
    """
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

#TODO: CREATE THIS FUNCTION
def ingest_csv_data(filename: str):
    """Given a CSV file, it ingests the data into the utsc-execise.db file.

    Keyword arguments:
    filename: the name of the CSV file that you want to ingest into the database.
    """

    try:
       logger.info("Connecting to the database")
       db_connection = connect_to_db("utsc-exercise.db")
       
       logger.info(f"Loading CSV data from {filename}")
       df = pd.read_csv(filename)
       
       logger.info("Cleaning the dataframe")
       cleaned_df = remove_unnamed_columns(df)
       
       logger.info("Inserting data into the Employee table")
       insert_employee_data_into_db(db_connection, cleaned_df)
       
       logger.info(f"Moving {filename} to the hist folder")
       shutil.move(filename, f"hist/{filename}")
       
       logger.info("CSV data ingestion completed successfully")
   
    except Exception as e:
       logger.error(f"An error occurred while ingesting CSV data: {e}")

    

def print_employee_dataframe():
    """Connects to the database, puts the Employee table into a dataframe, and then prints the dataframe.
    Use this for any sort of validation.
    Once you complete the 
    """
    db_connection = connect_to_db("utsc-exercise.db")
    df = pd.read_sql("SELECT * FROM EMPLOYEE ORDER BY EMPLOYEEID DESC", con=db_connection)
    print(df)

if __name__ == '__main__':
    #TODO: UNCOMMENT THIS TO INGEST THE DATA ONCE YOU HAVE COMPLETED THE FUNCTION ABOVE
    ingest_csv_data("legacy_employees.csv")
    print_employee_dataframe()