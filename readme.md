# UTSC MGTC28 Exercise

Hi Everyone, this exercise is to allow you to get some experience on some type of requests you may get once you enter the workforce. As a newbie to the organization, your team is likely going to ask you to do some small tasks to get you situated with the project. This can include fixing some small bugs, adding a nice-to-have feature, or doing a quick lookup of some data.

## The Scenario

You just joined the HR team at Caynze Corp in a junior data analyst/developer capacity. To get you to understand the dataset and the application that you'll likely be working with day-to-day, your supervisor has asked you to do the following tasks:

1. There seems to be a bug in the streamlit application (main.py, see details below on how to run), resolve the error so that the graph will load.
2. As you may notice on the streamlit application, there are currently 5000 employees in the database. We have some old CSV data that we haven't added into our database. Add the employees from legacy_employees.csv to the employee table in the DB by creating the new function highlighted in db_setup.py.
3. On the streamlit application, the team wants some new data to be displayed:
   - Add a new graph that displays the average salary by country.
   - Add a new graph that displays the number of employees by country.
   - Add a new graph that displays the number of employees by job title.

Your supervisor believes that there is enough documentation available to solve these tasks already within the code base. Use the tools available to you to complete these tasks!

### Running the Streamlit Application

---

In the src directory execute `python -m streamlit run ./main.py` in the terminal.

### Editing and Running the db_setup.py

---

When making changes to the db_setup.py, make sure to `cd` into the db folder.
The way I would do it in the terminal/command line is:

1. `cd db`
2. `python db_setup.py`
