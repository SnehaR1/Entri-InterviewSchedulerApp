#Interview Scheduler app

The system helps register candidate/user, interviewer and manager. Interviewers and users can add/register their availabilities ,which helps manager to generate slots when both the interviewer and candidate will be available.

#Steps to get it run locally

1.Make a virtual environment
->python -m virtualenv env

2.Activate Virtual environment
->env\Scripts\activate

3.Install The dependencies
->pip install -r requirements.txt
 
or 

I will list down the packages that I have installed for this project.

	a. Django==4.2.16
	b. django-cors-headers==4.6.0
	c. djangorestframework==3.15.2
	d. psycopg2-binary==2.9.10

install these as follows => "pip install <package  name>"

4.Configure database connections.
->Here I have used postgres for this project.
->The configuration is added in the code make changes to the values as needed.

5.Make necessary migrations using the following commands -> "python manage.py makemigrations" and "python manage.py migrate" 

6.Run the project using the command -> "python manage.py runserver"

#API Documentation

-> POST /api/register/
-> Description : This endpoint helps register user/candidate, interviewer and manager.

->Request : 

+----------------+----------------------------------------------------------+------------+
| Parameter      | Description                                              | Type       |
+----------------+----------------------------------------------------------+------------+
| username       | Valid name. Should not be empty.                         | String     |
| role           | valid roles include "user","interviewer" and "manager" . | String     |  
		                 Should not be empty.             			          
| password       | Valid password.Should not be empty.                      | String     |                                 
+----------------+----------------------------------------------------------+------------+

->Response : 

+----------------+----------------------------------------------------------+
| parameter      | Description                                              |
+----------------+----------------------------------------------------------+
| 200            | Success                                                  |
| 400            | Error Bad Request                                        |
+----------------+----------------------------------------------------------+

-> POST /api/register_availability/
-> Description : This endpoint helps candidates and interviewers to register their availability.

->Request : 

+----------------+----------------------------------------------------------+------------+
| Parameter      | Description                                              | Type       |
+----------------+----------------------------------------------------------+------------+
| canidate_id/   | Valid candidate id or interviewer id should be provided. | Int        |
  Interviewer id | based on who id registering the availability.            |            |
|                |  Should not be empty                                     |            |
| interview_date | valid roles include "user","interviewer" and "manager" . |            |
                  Should nto be empty                                       | String     |  
		                     			                                                        
| start_time     | user can provide from what time they will be available.  |            |
                  Should not be empty                                       | String     | 
| end_time       | user can provide until what time they will be available. |            |
                   should not be empty                                      | String     |   
+----------------+----------------------------------------------------------+------------+

->Response : 

+----------------+----------------------------------------------------------+
| parameter      | Description                                              |
+----------------+----------------------------------------------------------+
| 200            | Success                                                  |
| 400            | Error Bad Request                                        |
+----------------+----------------------------------------------------------+

-> POST /api/generate_slots/
-> Description : This endpoint helps generate slots where both candidate and interviewer will be available , candidates id  and interviewers id is to be inputted for this.

->Request : 

+----------------+----------------------------------------------------------+------------+
| Parameter      | Description                                              | Type       |
+----------------+----------------------------------------------------------+------------+
| canidate_id and | Valid candidate id or interviewer id should be provided. | Int       |
  Interviewer id |   Should not be empty                        
+----------------+----------------------------------------------------------+------------+

->Response : 

+----------------+----------------------------------------------------------+
| parameter      | Description                                              |
+----------------+----------------------------------------------------------+
| 200            | Success                                                  |
| 400            | Error Bad Request                                        |
+----------------+----------------------------------------------------------+
