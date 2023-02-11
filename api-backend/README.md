# Intelliq Api-Backend

## Requirements
All dependencies for using the Api-Backend are contained in [venv_dependencies.txt](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/venvdependencies.txt).  
To install the dependencies, run the following command on a terminal:  
`pip install -r ./venvdependencies.txt`
## Set up the Server
* First set up the database(check [here](https://github.com/ntua/SoftEng22-12/tree/main/data#readme) for instructions).
* Then open a terminal in the current directory and run the following command to start the server:  
`python .\service.py`

## Documentation
Documentation for the Intelliq Api-Backend can be found in the postman collections included in the [test](https://github.com/ntua/SoftEng22-12/tree/main/test) directory.
## Components

### Authorisation Endpoints

Authorization Endpoints implementations are contained in the [Users](https://github.com/ntua/SoftEng22-12/tree/main/api-backend/Users) folder. They consist of:
* **[loginout.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Users/loginout.py)** : Contains implemantations for the login and logout endpoints

### Administrative Endpoints

Admin Endpoints implementations are contained in the [Admin](https://github.com/ntua/SoftEng22-12/tree/main/api-backend/Admin) folder and can only be accessed by users with the administrator role. They consist of:
* **[healthcheck.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Admin/healthcheck.py)**:  
Contains implementation of healthcheck endpoint.

* **[questionnaire_upd.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Admin/questionnaire_upd.py)**:  
Contains implementation of questionnaire_upd endpoint.

* **[resetall.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Admin/resetall.py)**:  
Contains implementation of resetall endpoint.

* **[resetq.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Admin/resetq.py)** :  
Contains implementation of resetq endpoint.

* **[usermod.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Admin/usermod.py)** :  
Contains implementations of usermod and users endpoints.
 
### User Endpoints

User Endpoints implementations are contained in the [Users](https://github.com/ntua/SoftEng22-12/tree/main/api-backend/Users) folder. They consist of:
* **[questionnaireid.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Users/questionnaireid.py)** :  
Contains implementation of questionnaire endpoint.

* **[question.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Users/question.py)** :  
Contains implementation of question endpoint.

* **[doAnswer.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Users/doAnswer.py)** :  
Contains implementation of doanswer endpoint.

* **[getsessionanswers.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Users/getsessionanswers.py)** :  
Contains implementation of getsessionanswers endpoint.

* **[getquestionanswers.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Users/getquestionanswers.py)** :  
Contains implementation of getquestionanswers endpoint.

### Frontend Endpoints

* **[getallanswers.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/Users/getallanswers.py)** :  
Contains implementation of getallanswers endpoint.

* **[service.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/service.py)** :  
Contains implementations of getQuestionnaires, getSessions and getQuestions endpoints.

### Other files

* **[authentication.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/authentication.py)** :  
Contains authUser and authAdmin methods that are used for user authentication.

* **[create_venv_windows.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/create_venv_windows.py)** :  
Script that deploys a virtual environment in the directory that it's executed.

* **[csvResponse.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/csvResponse.py)** :  
Generates a response for returning a csv file.

* **[mysqlconfig_template.py](https://github.com/ntua/SoftEng22-12/blob/main/api-backend/mysqlconfig_template.py)** :  
Contains a template for configuring the database connection.