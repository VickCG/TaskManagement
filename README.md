# Task Manager API

> A FastAPI-based task management application with JWT-based authentication, role-based access control, and PostgreSQL integration.

---

## Table of Contents

1. [About](#about)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Environment Variables](#environment-variables)
   - [Running the Application](#running-the-application)
   - [Testing](#testing)

---

## About

This project is a backend API for managing tasks, built with **FastAPI**. It includes features like user authentication, role-based access control, and task management. The API is designed to be scalable, secure, and easy to deploy with Docker.

---

## Features

- **JWT Authentication**: Secure login and token-based authentication.
- **Role-Based Access Control**: Separate permissions for employers, and employees.
- **Task Management**: CRUD operations for tasks.
- **PostgreSQL Integration**: Uses SQLAlchemy for ORM.
- **Swagger UI**: Auto-generated API documentation.
- **Docker Support**: Easy deployment using Docker Compose.

---

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Containerization**: Docker & Docker Compose
- **Environment Management**: Python dotenv

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Docker & Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/VickCG/TaskManagement.git
   cd TaskManagement
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your configurations:

   ```env
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_DB=
   DATABASE_URL=
   SECRET_KEY=
   ALGORITHM=
   ACCESS_TOKEN_EXPIRE_MINUTES=
   ```

### Running the Application

#### Using Docker

1. Build and run the services:

   ```bash
   docker-compose up --build
   ```

2. The application will be available at:

   ```
   http://127.0.0.1:8000
   ```

3. Access the Swagger UI for API documentation:

   ```
   http://127.0.0.1:8000/docs
   ```

### Testing

Run the test suite using `pytest`:

```bash
pytest
```
