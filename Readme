# Event Management System

This is an Event Management System built with Django, using SQLite as the database. It allows users to create, update, delete, and list events, and manage event requests. The project is containerized using Docker and includes automatic API documentation with Swagger.

## Features

- User authentication (login required to create, update, or delete events)
- Event creation and management (create, update, delete events)
- Manage event requests (approve or decline)
- List available, own, and participated events
- Email notifications for event request approvals/declines
- API documentation generated using Swagger ( http://localhost:8000/swagger/ )

## Requirements

Before you begin, ensure you have the following installed:

- Docker
- Docker Compose

## Getting Started

1. Clone this repository:

    git clone https://github.com/LukashOleksii/EventManagementApp.git

2. Build and run the Docker containers:
    
    docker-compose up --build

    This will build the Docker image, install dependencies, and start the Django development server on http://localhost:8000. You can visit web aplication and try how it is works.

3. Running Migrations

    docker-compose exec web python manage.py migrate

4. Running script for populate DB with test data

    docker-compose exec web python manage.py populate_db


