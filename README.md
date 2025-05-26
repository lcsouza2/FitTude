# FitTude

FitTude is a comprehensive workout tracking application built with FastAPI that helps users manage their fitness routines, track exercises, and monitor progress.

## Features

- User authentication with JWT tokens
- Email verification for registration and password reset
- Rate limiting and security measures
- Workout plan management
- Exercise tracking with sets and reps
- Equipment and muscle group organization 
- Progress reporting
- Caching with Redis
- PostgreSQL database storage

## Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy (with async support)
- Redis
- PostgreSQL
- Poetry for dependency management
- JWT for authentication
- FastAPI Mail for email services
- Pytest for testing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FitTude
```

## Directory Structure

FitTude/
├── app/
│   ├── core/          - Core functionality
│   ├── database/      - Database models and migrations
│   ├── routes/        - API route handlers
│   └── main.py        - Application entry point
├── templates/         - Email templates
├── tests/             - Test suites
└── pyproject.toml     - Project configuration