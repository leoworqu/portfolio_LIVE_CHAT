# portfolio_LIVE_CHAT

Flask Live Chat App
Description
Welcome to the Flask Live Chat App! This application is designed to provide a real-time chat experience using Flask, a popular web framework for Python. Users can engage in live conversations, register and log in, and enjoy a secure and interactive chat environment.


Team
Leul Habteselassie - Lead Developer


Project Setup
Requirements
To get started, you need to install the necessary dependencies. This project uses a requirements.txt file to manage dependencies.


Architecture
The Flask Live Chat App follows a typical architecture with the following components:

    Backend
        Flask: The main web framework used to handle routing, request processing, and server-side logic.
        Flask-SQLAlchemy: Used for database management and ORM (Object-Relational Mapping). It simplifies database interactions and helps in managing the application's data.
        Flask-WTF: Provides a set of tools for handling forms, including validation and CSRF protection.
        Flask-Login: Manages user sessions and authentication, ensuring secure access to user-specific data.
        Flask-Bcrypt: Handles password hashing and encryption, adding a layer of security for user credentials.
    Frontend
        HTML/CSS/JavaScript: Standard web technologies used for building the user interface. The chat messages and user interactions are dynamically updated using JavaScript.
        Third-Party Services
        Email-Validator: Validates email addresses to ensure they are in a proper format and prevent invalid entries.


Project Structure
Here's a brief overview of the project's folder structure:

PORTFOLIO_LIVE_CHAT/
│
├── chatapp/
│   ├── __init__.py          # Initializes the Flask app and sets up configurations
│   ├── models.py            # Database models
│   ├── routes.py            # Routes and view functions
│   ├── forms.py             # Forms used in the application
│   ├── static/              # Static files (CSS, JS, images)
│   └── templates/           # HTML templates
│
|── app.py                   # Entry point
├── requirements.txt         # List of dependencies
└── README.md                # This file


Thank you for checking out the Flask Live Chat App! We hope you find it useful and enjoyable. If you have any questions or need further assistance, feel free to reach out. Happy chatting!