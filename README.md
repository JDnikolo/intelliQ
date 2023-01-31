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
* Set up the database:  
`mysql < ./data/schema.sql`
* Add DB user credentials to `./api-backend/mysqlconfig_template.py` and rename it to `mysqltemplate.py`.
* Setup the Vue frontend:  
`cd ./frontend/intelliq-frontend`   
`npm install`

## Server Start

## Component Descriptions

### [api-backend](https://github.com/ntua/SoftEng22-12/tree/main/api-backend#readme)

### [cli](https://github.com/ntua/SoftEng22-12/tree/main/cli#readme)

### [data](https://github.com/ntua/SoftEng22-12/tree/main/data#readme)

### [frontend](https://github.com/ntua/SoftEng22-12/tree/main/frontend#readme)

### test

### vpp

## TODOs:
* join API-CLI dependencies into a single file?
* change to final DB schema name  