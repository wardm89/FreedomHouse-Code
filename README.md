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