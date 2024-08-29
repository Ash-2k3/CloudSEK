# CloudSEK Project

## Introduction

Welcome to the Ashwath's CloudSEK SDE Backend Internship Task's solution! This application allows users to create, read, and comment on posts.

## Tech Stack Used

- **Flask:** Micro web framework for Python.
- **SQLAlchemy:** An ORM for database management.
- **JWT (JSON Web Tokens):** For secure authentication.
- **SQLite:** The database used for storing data.
- **Werkzeug:** A comprehensive WSGI web application library.

## File Structure

Here’s an overview of the project’s file structure:
```
app/ ├── init.py # Application factory
     ├── models.py # Database models
     ├── routes.py # API routes
     ├── config.py # Configuration settings instance/

instance/ ├── app.db # SQLite databas

populate_datastore_with_sample_data.py # Script to populate database with sample data
run.py # Script to start the server
.gitignore # Git ignore file
```

## Installation

To get started with this project on macOS, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Ash-2k3/CloudSEK.git
    cd CloudSEK
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Starting the Server

To run the server:

1. **Run the Server:**

    ```bash
    python run.py
    ```

2. **Populate the Datastore (Optional):**

    Before starting the server or while it’s running, you can populate the database with sample data using:

    ```bash
    python populate_datastore_with_sample_data.py
    ```

    This will add sample posts and comments to your database for testing purposes.

## Available Endpoints

Here’s a quick overview of the available endpoints:

- **`POST /register`** - Register a new user. Requires `username` and `password`.
- **`POST /login`** - Log in to receive a JWT token. Requires `username` and `password`.
- **`POST /posts`** - Create a new post. Requires JWT and `title`, `content`.
- **`GET /posts`** - Retrieve all posts. JWT required.
- **`GET /posts/<int:post_id>`** - Retrieve a specific post by ID. JWT required.
- **`POST /posts/<int:post_id>/comments`** - Add a comment to a post. Requires JWT, `content`.

**Note:** To obtain a JWT token, register and log in to receive your token. Include this token in the `Authorization` header for endpoints that require authentication.

## How to Test

To test the endpoints, you can use tools like [Postman](https://www.postman.com/) to make API requests.

You can also watch the following videos for a demonstration in which I have tested the API endpoints using Postman:
- [Video 1: Testing User Registration](https://github.com/Ash-2k3/CloudSEK/blob/main/screen-recordings/Register%20API.mp4)
- [Video 2: Testing User Login](https://github.com/Ash-2k3/CloudSEK/blob/main/screen-recordings/Login%20API.mp4)
- [Video 3: Testing Post Creation](https://github.com/Ash-2k3/CloudSEK/blob/main/screen-recordings/Create%20Post%20API.mp4)
- [Video 4: Testing Post Retrieval - By IDs & All](https://github.com/Ash-2k3/CloudSEK/blob/main/screen-recordings/Get%20Posts%20API.mp4)
- [Video 5: Creating Comments](https://github.com/Ash-2k3/CloudSEK/blob/main/screen-recordings/Create%20Comment%20API.mp4)
- [Video 6: Populating Dummy Data](https://github.com/Ash-2k3/CloudSEK/blob/main/screen-recordings/Populating-Dummy-Data-Script.mp4)

## Acknowledgements

Thank you for taking the time to review my code. Happy coding!
