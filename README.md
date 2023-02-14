# Software Engineering Project 2022-2023

**Group**: softeng2022-12  
**Members**: el19955, el19890, el19156, el19085, el17514, el15170
  
el19955: Athanasios Tsimpis  
el19890: Nikolaos Karafyllis  
el19156: Christos Psallidas  
el19085: Evangelos Myrgiotis  
el17514: Nondas Floros  
el15170: Ioannis Nikolopoulos  

# **intelliq**

## Prerequisites
The following software is required to build and run this project:   
* Python 3.10 (or newer) with pip 22.3.1 (or newer)
* Node v18.12.1 (or newer) with NPM 8.10.0 (or newer)
* MySQL Server 8.0  

The environments running the api-backend server and the CLI have their respective requirements, which are covered in the Installation section.
## Deployment
* Clone this repository, and change into its main directory.
* Install api-backend dependencies:  
`pip install -r ./api-backend/venvdependencies.txt`
* Install CLI dependencies:   
`pip install -r ./cli/requirements.txt`
* Add cli directory to PATH (see CLI README).
* Set up the database:  
`mysql < ./data/schema.sql`
* Add main admin to the database, using the credentials provided by our staff.   
* Add DB user credentials to `./api-backend/mysqlconfig_template.py` and rename it to `mysqltemplate.py`.
* Setup the Vue frontend:  
`cd ./frontend/intelliq-frontend`   
`npm install`
* Add ./cli to PATH on the appropriate environment if you intend to use access the service via the CLI. (platform specific)

## Starting the Service  
* Ensure the MySQL server is up and running.  
* Start the Flask backend:  
`flask --app service.py -p 9103`  
You can now access the service using the CLI.
* Start the Vue frontend server:  
`cd ./frontend/intelliq-frontend`   
`npm run dev`  
You can now access the service via web browser on [https://localhost:5173/](https://localhost:5173/) for responding to questionnaires, and [https://localhost:5173/viewer](https://localhost:5173/viewer) for accessing results.  

## Component Descriptions  
  
You can find detailed descriptions of each component in their respective folders:    
  
### [api-backend](https://github.com/ntua/SoftEng22-12/tree/main/api-backend#readme)  
The service's REST API backend.    
### [cli](https://github.com/ntua/SoftEng22-12/tree/main/cli#readme)
The service's Command Line Interface. Includes Pytest scripts for unit and functional testing of the CLI.  
### [data](https://github.com/ntua/SoftEng22-12/tree/main/data#readme)
DDL and DML scripts for configuring the service's MySQL database.  
### [frontend](https://github.com/ntua/SoftEng22-12/tree/main/frontend#readme)
The service's frontend server, implemented using Vue.  
### [test](https://github.com/ntua/SoftEng22-12/tree/main/test)
Postman scripts for running tests on the API endpoints and dummy questionnaire files used for testing.
### [vpp](https://github.com/ntua/SoftEng22-12/tree/main/vpp)  
The updated Visual Paradigm project file(s) describing the service, written in Greek.  
