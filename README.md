# Vehicle Rental Management System

A production-ready backend infrastructure developed using the FastAPI framework. This project focuses on providing a secure and scalable RESTful API for vehicle fleet management, rental tracking, and multi-level user authorization.

## Project Overview
The system is designed to handle the complexities of a rental business, ensuring that data integrity is maintained through strict validation and that sensitive operations are protected via Role-Based Access Control (RBAC).

## Core Functionality

### 1. Security & Authentication
* **Password Encryption**: Employs Bcrypt hashing to ensure user credentials remain encrypted at rest.
* **Session Management**: Implements stateless authentication using JSON Web Tokens (JWT) for secure client-server communication.

### 2. Fleet & Rental Operations
* **Inventory Control**: Real-time tracking of vehicle availability across the fleet.
* **Automated State Updates**: The system handles the transition of vehicle availability status during rental transactions to prevent conflicts.

### 3. Administrative Governance
* **Privileged Access**: Restricted endpoints for inventory expansion and record management.
* **Authentication Guards**: Middlewares that verify administrative status before allowing access to sensitive logic.

## Technical Architecture

* **Language & Framework**: Python / FastAPI
* **Persistence Layer**: SQLite database managed through SQLAlchemy ORM
* **Schema Validation**: Pydantic models for request/response serialization
* **Environment**: Uvicorn ASGI server

## File Structure & Assets
* `main.py`: Entry point of the application containing core API routes.
* `admin.py`: Utility for administrative bootstrapping and privileged setup.
* `Vehicle_Rental_System_Technical_Report.pdf`: Comprehensive documentation including architectural diagrams and endpoint logic.

## Documentation
For a deep dive into the system's design patterns and security implementation, please review the Technical Report included in the repository root.
