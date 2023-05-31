Running the FastAPI Project
===========================

This guide will walk you through setting up and running this project on your local machine.


# Running survival_backend

This document provides instructions for setting up and running this project on your local machine.

## Pre-requisites

Before starting, ensure that you have the following software installed:

- Python 3.7 or higher
- pip (Python package installer)
- virtualenv

## Instructions

### 1. Set Up a Virtual Environment

First, navigate to the project directory in your terminal. Once inside the project directory, create a new virtual environment using `virtualenv`:

```
python3 -m venv venv
```

This command creates a new virtual environment in a folder named `venv` within your project directory.

To activate the virtual environment:

On Windows, execute:

```
.\venv\Scripts\activate
```

On Unix or MacOS, execute:

```
source venv/bin/activate
```

### 2\. Install Dependencies

With the virtual environment activated, install the project dependencies using pip:


```pip install -r requirements.txt```

### 3\. Set Up Environment Variables

Create a file named `````.env``` in the root of the project directory with the following content:

shell

```DATABASE_USER=<your_database_user>
DATABASE_PASSWORD=<your_database_password>
DATABASE_HOST=<your_database_host>
DATABASE_NAME=<your_database_name>
```

Replace `<your_database_user>`, `<your_database_password>`, `<your_database_host>`, and `<your_database_name>` with your actual database credentials.

### 4\. Run the Application

Finally, you can run the application with the following command:


`uvicorn main:app --reload`

The FastAPI server should now be running on your local machine at `http://localhost:8000`. You can view the interactive API documentation at `http://localhost:8000/docs`.