# Intelliq CLI

## Requirements
On a python terminal, run:
`pip install -r requirements.txt`

## Using the CLI
First open a git bash terminal in the cli directory and run:

`export PATH="$PATH:path/ending/with/SoftEng22-12/cli"`

then you can use the cli with commands of the following format:

`se2212 scope [--argument1] [--argument2] ... --format csv/json` 

example:

`se2212 healthcheck --format csv`

## Tests
To run the Cli tests, open a Python terminal in the cli directory (./cli) and execute the following command:
`pytest ./cli_tests`

## Exam Script
run exam_script:
  `bash exam_script`