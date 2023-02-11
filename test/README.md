# Intelliq Testing Specifications

## Requirements
* Postman tests written in Postman for Windows Version 10.8.8
* x64 Architecture
* Each collection has its own requirements, specified under the appropriate collection chapter

### 1. Exam collection

#### Requirements
* This collection was designed to run after the exam script and assumes that the database is in the exact state that the script has rendered.
* An admin with the username "andreane82" and a functioning access_token, specified in the API testing documentation is supposedely existing in the database.
* The "Trekking Club" questionnaire is supposedely existing in the database.

The exam test collection workflow is the following:
1. The admin checks for the server's health
2. An answer to the "Trekking Club" questionnaire is given by anonymous user for a certain session.
3. The admin sends a request to get the answers of the "Trekking Club" questionnaire answered in the session of step 2.

### 2. User Endpoints collection

#### Requirements
* To replicate the test runs in this collection, the database must be clean.
* An initial request to upload the "Trekking Club" questionnaire is sent, following requests need to perform operations on some data, that is why this step is obligatory.
* An admin with the username "andreane82" and a functioning access_token, specified in the API testing documentation is supposedely existing in the database.

The user endpoints collection test the following requests:
1. POST doanswer/:questionnaireID/:questionID/:sessionID/:optionID
2. GET questionanswers/:questionnaireID/:session?format={json,csv}
3. GET getquestionanswers/:questionnaireID/:questionID?format={json,csv}
4. GET question/:questionnaireID/:questionID?format={json,csv}
5. GET questionnaire/:questionnaireID

**After this, the database does not need any further modifications to run the rest of the tests**

### 3. Frontend-only Endpoints collection

#### Requirements
* None, as long as this collection runs after collection 2

The collection testing the endpoints made for the frontend application consists of the following requests:
1. GET getQuestionnaires
2. GET getSessions
3. GET getQuestions
4. GET getallanswers

### 4. Login/Logout collection
#### Requirements
* The admin must create a user to make all necessary checks with this user's credentials. This is the first request made in the collection, so this collection can be tested by itself or with the rest

The collection tests the login/logout functionality under numerous scenarios. The requests are:
1. POST login
2. POST logout

### 5. Other collection
#### Requirements
* An admin with the username "andreane82" and a functioning access_token, specified in the API testing documentation is supposedely existing in the database.
* A questionnaire with questionnaireID "QQ000" and some answers in it.

This collection tests a variety of endpoints and functionalities as standalones.

### 6. Admin Endpoints Collection
#### Requirements
* An admin with the username "andreane82" and a functioning access_token, specified in the API testing documentation is supposedely existing in the database.

Due to the positioning of the tests no furthers requirements are needed for this endpoint. The requests tested are:
1. POST admin/usermod/:user/:password
2. GET admin/usermod/users/:user
3. GET admin/healthcheck
4. POST admin/questionnaire_upd
5. POST admin/resetq/:questionnaireID
6. POST admin/resetall
