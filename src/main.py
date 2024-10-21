import pandas as pd
import streamlit as st
import sqlite3

def get_employee_salaries():
    db_connection = sqlite3.connect('./db/utsc-exercise.db')
    employee_salary_df = pd.read_sql("""SELECT e.*, s.YearlyCompensation, cm.Country, e.FirstName + ' ' + e.LastName as FullName
                                                FROM EMPLOYEE e 
                                                LEFT JOIN Salary s ON e.EmployeeId = s.EmployeeId
                                                LEFT JOIN OfficeCountryMapping cm ON cm.OfficeId = e.OfficeId
                                            """, db_connection)
    db_connection.close()
    return employee_salary_df



def get_avg_salary_by_job_title(employee_salary_df: pd.DataFrame):
    """Creates the multi-select filter widget to select job titles, and creates the graph that displays
    average salary by job title
    """
    # Get unique job titles from the dataframe
    job_titles = employee_salary_df['JobTitle'].unique()

    # Create a multi-select widget for filtering job titles
    selected_titles = st.multiselect('Select Job Title', job_titles, default=job_titles)

    # Filter the dataframe based on selected job titles
    filtered_df = employee_salary_df[employee_salary_df['JobTitle'].isin(selected_titles)]

    # Group by JobTitle and calculate the average salary
    avg_salary_by_job_title = filtered_df.groupby('JobTitle')['YearlyCompensation'].mean().reset_index()
    
    #Plot the graph
    st.subheader("Average Salary by Job Title")
    st.bar_chart(avg_salary_by_job_title, x = 'JobTitle', y = 'YearlyCompensation', x_label='Job Title', y_label='Yearly Salary', color='#3ac21f')



def get_avg_salary_by_country(employee_salary_df: pd.DataFrame):
    countries = employee_salary_df['Country'].unique()

    selected_countries = st.multiselect('Select Country', countries, default=countries)

    filtered_df = employee_salary_df[employee_salary_df['Country'].isin(selected_countries)]

    avg_salary_by_country = filtered_df.groupby('Country')['YearlyCompensation'].mean().reset_index()

    #Plot the graph
    st.subheader("Average Salary by Country")
    st.bar_chart(avg_salary_by_country, x = 'Country', y = 'YearlyCompensation', x_label='Country', y_label='Yearly Salary', color='#3ac21f')


def create_name_salary_lists(employee_salary_df):
    names_list = employee_salary_df['FullName'].tolist()
    salaries_list = employee_salary_df['YearlyCompensation'].tolist()

def find_person_with_salary_from_list(target_salary, salary_list, name_list):
    pass

if __name__ == '__main__':
    # Streamlit app title
    st.title('Employee Salary Analysis')

    #Salary DataFrame
    employee_salary_df = get_employee_salaries()
    
    #Avg salary by job title graph
    get_avg_salary_by_job_title(employee_salary_df)
    
    get_avg_salary_by_country(employee_salary_df)

    st.chat_input("Hello")

    st.write(f"Employee with the target salary = Aarij")