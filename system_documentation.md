# User Management System Documentation

## Overview
The User Management System is a FastAPI-based application for managing user accounts, authentication, and role-based access control.

## API Endpoints

### User Management

#### PUT /users/{user_id}/profile
**Description:** Updates the authenticated user's profile information.  
**Authorization:** Requires the user to be authenticated and updating their own profile.  
**Request Body:** UserUpdate schema (e.g., first_name, last_name, bio, linkedin_profile_url).  
**Response:** UserResponse with updated user data and HATEOAS links.  

**Example:**
```bash
curl -X PUT "http://localhost/users/123e4567-e89b-12d3-a456-426614174000/profile" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"first_name": "John", "last_name": "Doe", "bio": "Software developer"}'
```

#### POST /users/{user_id}/professional-status
**Description:** Upgrades a user to professional status, sending an email notification.  
**Authorization:** Requires ADMIN or MANAGER role.  
**Response:** UserResponse with updated user data and HATEOAS links.  

**Example:**
```bash
curl -X POST "http://localhost/users/123e4567-e89b-12d3-a456-426614174000/professional-status" \
     -H "Authorization: Bearer <admin_token>"
```

## Database Schema
- **users:** Stores user data, including `is_professional` for professional status.  
- **audit_logs:** (Added in RBAC Enhancements) Stores audit logs for role changes.  

## Email Templates
- **professional_status_upgrade.md:** Notification for professional status upgrades.  

# 🚀 User Management System - Technical Overview

Welcome to the User Management System, a powerful and scalable solution built using the FastAPI web framework! 🌟 This document provides a comprehensive overview of the system's architecture, key features, and implementation details. Let's dive in and explore the awesomeness! 😎

## 🏗️ Architecture

The User Management System follows a modular and layered architecture to ensure separation of concerns and promote maintainability and scalability. The core components include:

- **FastAPI Application**: The main entry point of the application, handling API requests and responses.
- **Database Layer**: Utilizes SQLAlchemy ORM for efficient database interactions and data persistence.
- **Alembic**: Used for seamless database migrations.
- **Service Layer**: Contains the business logic and core functionalities of the application.
- **API Layer**: Defines the API endpoints, request validation, and response serialization.
- **Authentication and Authorization**: Implements OAuth2 with Password Flow for secure user authentication and role-based access control.
- **Email Service**: Handles email notifications and verification, with support for email templates.

## 💪 Best Practices and Standards

The project adheres to industry best practices and coding standards to ensure code quality, clarity, and maintainability:

- **PEP 8**: Consistent code formatting for improved readability.
- **Type Hints**: Enhances code clarity and catches potential type-related issues.
- **Dependency Injection**: Promotes loose coupling and testability.
- **Asynchronous Programming**: Efficient handling of concurrent requests.
- **Error Handling and Logging**: Robust error handling and debugging capabilities.
- **Testing with Pytest**: Comprehensive unit and integration testing.
- **Containerization with Docker**: Seamless deployment and scalability.

## 🌟 Key Features

### 👥 User Management

- ✅ User registration and login functionality (needs more testing)
- 🔑 User roles and permissions: Admin, Manager, Authenticated, Anonymous (needs more testing)
- 🍞 User account management (BREAD operations)
- 📧 Email verification for registered user accounts
- 🔒 First user automatically becomes admin (to be converted to a command-line program in the future)

### 📜 API Design and Documentation

- 🌐 RESTful API endpoints for user management
- 📝 Swagger/OpenAPI documentation for easy API exploration and integration
- 🔐 Secure authentication and authorization using OAuth2 with Password Flow

### 🗄️ Database Integration

- 🐘 Integration with PostgreSQL database using SQLAlchemy ORM
- ⚡ Efficient and scalable database design for user management
- ⏩ Asynchronous database operations for improved performance

### 📧 Email Notifications

- 📬 Email templates for user verification and other notifications
- 🎨 Easily customizable email templates with headers and footers
- 🔍 Integration with Mailtrap for email testing and viewing in a test account

### 🧪 Testing and Quality Assurance

- 🔍 Comprehensive test suite for unit testing and integration testing
- 🔧 Fixtures for setting up test data and mocking dependencies
- 🚀 Continuous Integration and Continuous Deployment (CI/CD) pipeline with GitHub Actions

### 🚀 Deployment and Containerization

- 🐳 Dockerization of the application for easy deployment and scalability
- 📦 Docker Compose for managing multi-container setup
- ⚙️ GitHub Actions workflow for automated testing and deployment

### 🔐 Administrator User Creation

- 🔑 Automatic assignment of administrator role to the first user created in the system
- ⚠️ Implemented for development and testing purposes, to be converted to a command-line program for security

### 🌐 CORS Support

- 🔀 Basic CORS support, although not configured for a specific domain

## 🆕 Features to be developed and tested

### 🆔 Username Generation (needs more testing)

- 🔀 Users are assigned a random username upon creation
- 🌐 Username is generated based on a combination of nouns, verbs, and a number
- ✏️ Users can change their username, but it must be unique
- 🔍 Username serves as a URL-safe identifier for posts and public information
- 🔒 Ensures user anonymity and privacy, if desired
- ⚠️ Needs more testing and verification

### 🌟 Pro Status Upgrade (needs additional development pro status is added to the schema and has some functionality)

- 🆙 Users can request to upgrade to pro status
- 📝 Users must fill out their complete profile to be verified as a pro
- 🔍 Pro status will be used for various purposes in the future
- 🔐 Upgrade request and verification process needs to be implemented

[Additional Features Required](features.md)

## 📜 Open Source and MIT License - [Here](https://github.com/kaw393939/user_management/blob/main/license.txt)

The User Management System is open-sourced under the MIT License, allowing for free use, modification, and distribution of the codebase. By making the project open source, it encourages:

- 🤝 Collaboration and knowledge sharing
- 🌍 Community contribution and improvement
- 🎓 Flexibility for students and developers to learn from and build upon the project

## 🚀 Let's Build Something Amazing!

We hope this technical overview has given you a comprehensive understanding of the User Management System. With its robust architecture, best practices, and exciting features, it provides a solid foundation for building scalable and secure user management solutions.

Feel free to explore the codebase, contribute to the project, and unleash your creativity! If you have any questions or suggestions, don't hesitate to reach out. Happy coding! 💻✨

