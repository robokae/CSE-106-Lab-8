# CSE 106 Lab 8

Gradebook web application with create, read, update, and delete (CRUD) features. Created using HTML, CSS, JavaScript, and Flask.

## Features
* Login page
* Student view page
    * View all courses 
    * Add/remove courses
* Instructor view page
    * View currently teaching courses
    * View student grades for each course
        * Edit grade

## Getting Started

### Prerequisites
In order to run the web application, make sure to have the following installed:
* Git
* Python (3.8 or later)

### Viewing the Application
To run the application, execute the following commands in the command line:
```bash
# Clone the repository and access it
git clone https://github.com/robokae/CSE-106-Lab-8.git
cd CSE-106-Lab-8

# Create a Python virtual environment
python3 -m venv venv

# Activate Python virtual environment on macOS or Linux
source venv/bin/activate   

# Activate Python virtual on Windows
venv\Scripts\activate

# Install the dependencies
pip install -r requirements.txt

# Run the development server
flask run
```


