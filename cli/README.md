# Intelliq CLI

## Requirements
* All cli dependencies are contained in the [requirements.txt](https://github.com/ntua/SoftEng22-12/blob/main/cli/requirements.txt) file.

* To install the dependencies open a terminal and run:  
`pip install -r requirements.txt`

## Using the CLI
* First open a git bash terminal in the cli directory and run:  
`export PATH="$PATH:."`  

* Then you can use the cli with commands of the following format:  
`se2212 scope [--argument1] [--argument2] ... --format csv/json` 

* Example:  
`se2212 healthcheck --format csv`

## Tests
* To run the Cli functional tests, open a Python terminal in the [cli](https://github.com/ntua/SoftEng22-12/tree/main/cli) directory **(./cli)**, then execute the following command:  
`pytest ./cli_tests`

* To run the Cli unit tests, open a Python terminal in the [cli_unit_tests](https://github.com/ntua/SoftEng22-12/tree/main/cli/cli_unit_tests) directory **(./cli/cli_unit_tests)**, then execute the following command:  
`pytest ./`

## Exam Script
* Run [exam_cli_script](https://github.com/ntua/SoftEng22-12/blob/main/cli/exam_cli_script):  
  `bash exam_cli_script`