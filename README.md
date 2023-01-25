# FreedomHouse-Code
Helper code for FH's website

## Getting Started
Make sure you have python version 3.7 installed or newer

Add Python extension if using VS Code

### Environment variables
Contact Matthew Ward to get this. Then add to the root of the project.

### Install virtual environment
    pip3 install virtualenv
    python3.7 -m venv .venv
    source .venv/bin/activate

### Install project dependencies
    pip3 install -r requirements.txt

### Updating Dependencies
Currently, everything in this repo shares the same dependencies. So the requirements.txt file lives at the root of the repo.

If you're adding new dependencies, run the following command to update the requirements.txt file for future development:

    pip3 freeze > requirements.txt

## High Level Logical Flow / Overview
Python script
1. Get all "Form_Responses" create <= 5 minutes ago
2. Get all the "Form_Response_Answers"
   1. Loop and add all the answers the the appropriate response
3. We now have a list of Form Responses with the corresponding answers to each question.
4. Get the Care_Cases (Pastoral Care Requests)
5. Check the title of the Care Case to see if it matches any the Form Responses
   1. If it does then skip that one. (It's already been created)
   2. If no Form Response matches an existing care case then CREATE one

[Pastoral Care Request Flow](Pastoral_Care_Request_Flow.png)