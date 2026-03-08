# Flask Task Management API

A RESTful API built with **Flask** that allows users to register, authenticate, and manage personal tasks securely.

This project demonstrates core backend development concepts including:

* Authentication using JWT
* Authorization (task ownership protection)
* CRUD operations
* Pagination
* Input validation
* RESTful API design

---

# Features

* User registration
* User login with JWT authentication
* Create tasks
* Retrieve tasks
* Update tasks
* Delete tasks
* Task ownership protection
* Pagination support
* Input validation and error handling

---

# Tech Stack

* Python
* Flask
* Flask-JWT-Extended
* SQLAlchemy
* SQLite

---

# Project Structure

```
flask-task-management-api
│
├── app/              # main application package
├── instance/         # SQLite database
├── run.py            # application entry point
├── config.py         # configuration settings
├── requirements.txt
└── README.md
```

---

# Installation

## Clone the repository

```
git clone https://github.com/abdulwahabdevs/flask-task-management-api.git
cd flask-task-management-api
```

## Create virtual environment

```
python -m venv venv
```

Activate it:

Mac / Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

## Install dependencies

```
pip install -r requirements.txt
```

## Run the application

```
python run.py
```

Server starts at:

```
http://127.0.0.1:5000
```

---

# Authentication

The API uses **JWT tokens**.

After logging in, include the token in protected requests:

```
Authorization: Bearer <your_token>
```

---

# API Endpoints

## Authentication

| Method | Endpoint       | Description                 |
| ------ | -------------- | --------------------------- |
| POST   | /auth/register | Register a new user         |
| POST   | /auth/login    | Login and receive JWT token |

## Tasks

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| POST   | /tasks/          | Create a task              |
| GET    | /tasks/          | Retrieve tasks (paginated) |
| GET    | /tasks/<task_id> | Retrieve a specific task   |
| PUT    | /tasks/<task_id> | Update a task              |
| DELETE | /tasks/<task_id> | Delete a task              |

---

# Pagination

Tasks support pagination using query parameters.

Example:

```
GET /tasks/?page=1&per_page=5
```

Example request:

```
curl -X GET "http://127.0.0.1:5000/tasks/?page=1&per_page=5" \
-H "Authorization: Bearer YOUR_TOKEN"
```

---

# Example Workflow

Typical API usage:

1. Register a user
2. Login to obtain a JWT token
3. Create tasks
4. Retrieve tasks with pagination
5. Update or delete tasks

---

# Future Improvements

* Automated testing with pytest
* API documentation (Swagger/OpenAPI)
* Docker containerization
* CI/CD pipeline
* Deployment

---

# License

This project is for educational and learning purposes.
