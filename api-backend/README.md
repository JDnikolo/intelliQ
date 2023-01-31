# Intelliq Api-Backend

## Requirements
All dependencies for using the Api-Backend are contained in [venv_dependencies.txt](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/venvdependencies.txt).    
To install the dependencies, run the following command on a terminal:  
`pip install -r ./venvdependencies.txt`
## Set up the Server
* First set up the database(check [here](https://github.com/ntua/SoftEng22-12/tree/main/data#readme) for instructions).
* Then open a terminal in the current directory and run the following command to start the server:  
`python .\service.py`

## Components

### Authorisation Endpoints:

Authorization Endpoints implementations are contained in the [Users](https://github.com/ntua/SoftEng22-12/tree/main/api-backend/Users) folder. They consist of:
* **login** :  
Accepts the username and the password of the user encoded in "application/x-www-form-urlencoded" format. If the authorization is successful, a json object that contains the user's access token is returned.

* **logout** :  
Logs out the user whose access token is contained in the HTTP header X-OBSERVATORY-AUTH. On success, it returns only status code 200(empty response body).

### Administrative Endpoints:

Admin Endpoints implementations are contained in the [Admin](https://github.com/ntua/SoftEng22-12/tree/main/api-backend/Admin) folder and can only be accessed by users with the administrator role. They consist of:
* **healthcheck**:  
Confirms end-to-end connectivity between the user and the database and returns the corresponding json object.

* **questionnaire_upd**:  
Enables the upload of a json file that contains data of a new questionnaire and then saves it in the system. The json file is labeled as a "file" field and must be encoded in multipart/form-data format.

* **resetall**:  
Resets all data of the system(questionnaires, answers and users). Returns corresponding json object on success and failure.

* **resetq/:questionnaireID** :  
Deletes all answers of the questionnaire with the given id(questionnaireID). Returns corresponding json object on success or failure.

* **usermod/:username/:password** :  
Adds a new user with the given credentials, changes the password of the user if the given username already exists.

* **users/:username** :  
Returns all information of the user with the given username. 

### User Endpoints:

User Endpoints implementations are contained in the [Users](https://github.com/ntua/SoftEng22-12/tree/main/api-backend/Users) folder. They consist of:
* **questionnaire/:questionnaireID** :  
Returns an object that contains the information and questions(ordered by ID) of the questionnaire with the given ID(questionnaireID).

* **question/:questionnaireID/:questionID** :  
Returns an object that contains all the information of the question with the requested ID(questionID) of the requested questionnaire(questionnaireID). The options of the question are ordered by their IDs.

* **doanswer/:questionnaireID/:questionID/:session/:optionID** :  
Registers the option(optionID) that was given in the current answer session(session) for the question with ID=questionID of questionnaire with ID=questionnaireID in the system. No object is returned and the session identifier consists of a string of 4 random characters.

* **getsessionanswers/:questionnaireID/:session** :  
Returns an object that contains all the answers that have been submitted in the questions of questionnaire with ID=questionnaireID during the requested answer session(session). Answers are sorted by the questions' ID.

* **getquestionanswers/:questionnaireID/:questionID** :  
Returns an object that contains all answers that have been submitted for all answer session of the question with ID=questionID of the questionnaire with ID=questionnaireID. All answers are ordered by time of submission.


