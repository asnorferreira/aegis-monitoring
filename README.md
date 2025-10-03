# Aegis - Industrial Infrastructure Monitoring Platform

Aegis is a full-stack web application designed for the real-time monitoring of industrial infrastructures. It provides a comprehensive dashboard to track the health of structures like bridges and buildings through sensor data analysis, enabling proactive maintenance and ensuring safety.

This project is a monorepo containing the frontend application (built with React/TypeScript) and the backend API (built with Python/Flask).

## Table of Contents

- [Features](#features)
- [Tech Stack & Architecture](#tech-stack--architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Demo Credentials](#demo-credentials)

## Features

- **Public-Facing Website**: A landing page with sections for Product, Pricing, and About Us.
- **Secure Authentication**: JWT-based authentication for client access.
- **Monitoring Dashboard**: An interactive dashboard displaying a list of all monitored infrastructures and their current status.
- **Detailed Structure View**: In-depth analytics for each structure, including real-time sensor data visualization.
- **Interactive Charts**: Time-series charts for various sensor types (Vibration, Strain, Temperature).
- **RESTful API**: A well-structured backend API with comprehensive documentation.

## Tech Stack & Architecture

### Backend

- **Language**: Python 3.13.7
- **Framework**: Flask
- **Architecture**: Clean Architecture, Domain-Driven Design (DDD) principles.
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **API Specification**: Swagger (via Flasgger)
- **Containerization**: Docker, Docker Compose

### Frontend

- **Language**: TypeScript
- **Framework**: React.js (with Vite)
- **UI Library**: Material-UI (MUI)
- **State Management**: Zustand
- **Charting**: Recharts
- **API Client**: Axios

## Project Structure

```
aegis-monitoring/
├── backend/                  # Python Flask Backend
│   ├── app/
│   │   ├── application/      # Use Cases / Services
│   │   ├── domain/           # Domain Models and Repository Interfaces
│   │   ├── infrastructure/   # DB Models, Repo Implementations, Seeding
│   │   └── presentation/     # API Endpoints (Blueprints) & Swagger Docs
│   ├── migrations/
│   ├── .env.example
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/                 # React TypeScript Frontend
    ├── public/
    ├── src/
    │   ├── api/              # Axios client and API calls
    │   ├── components/       # Reusable UI components
    │   ├── hooks/
    │   ├── layouts/
    │   ├── pages/            # Application pages (Landing, Dashboard, etc.)
    │   ├── services/         # State management stores (Zustand)
    │   ├── styles/
    │   ├── types/            # TypeScript type definitions
    │   └── App.tsx
    ├── .env.example
    └── package.json
```

## Prerequisites

- Docker and Docker Compose
- Node.js v24.9.0 and npm

## Getting Started

Follow these steps to get the application up and running locally.

### 1. Clone the Repository

```sh
git clone <your-repository-url>
cd aegis-monitoring
```

### 2. Backend Setup

The backend, database, and data seeding are fully containerized.

```sh
# Navigate to the backend directory
cd backend

# Create an environment file from the example
cp .env.example .env
```

Review the `.env` file and make changes if necessary (e.g., change `POSTGRES_PASSWORD`). The default values are configured to work out-of-the-box.

Now, build and run the containers using Docker Compose. This command will start the Flask API server, the PostgreSQL database, and run the database migrations and data seeding automatically.

```sh
docker-compose up --build
```

The backend API will be available at `http://localhost:5001`.

### 3. Frontend Setup

Open a **new terminal window**.

```sh
# Navigate to the frontend directory
cd frontend

# Create an environment file from the example
cp .env.example .env
```

The `.env` file should contain the base URL for the backend API. The default is already set correctly.

```
VITE_API_BASE_URL=http://localhost:5001/api
```

Install the dependencies and start the development server.

```sh
# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend application will be available at `http://localhost:3000`.

## API Documentation

Once the backend is running, the interactive Swagger API documentation is available at:

[**http://localhost:5001/apidocs**](http://localhost:5001/apidocs)

## Environment Variables

### Backend (`backend/.env`)

- `DATABASE_URL`: The connection string for the PostgreSQL database.
- `SECRET_KEY`: A secret key used for signing JWTs and sessions.
- `FLASK_ENV`: Set to `development`.

### Frontend (`frontend/.env`)

- `VITE_API_BASE_URL`: The full URL to the backend API's base path.

## Demo Credentials

To log in to the client dashboard, use the following credentials which are created by the database seeder:

- **Username**: `engineer@aegis.com`
- **Password**: `password123`