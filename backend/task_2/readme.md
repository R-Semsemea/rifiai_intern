This is a simple user authentication and registration REST API built with Flask, featuring:

User registration and login

Password hashing with bcrypt

Token-based authentication using JWT

Email notification on registration using IONOS SMTP

SQLite database for user storage


download the flask server and run it
there is a small UI in front folder to test or you can use postman collection as an example
edit .env values as you want

dependencies:
Flask

Flask-JWT-Extended

Flask-Mail

Flask-Bcrypt

Flask-SQLAlchemy

SQLite

dotenv for environment variables

CORS enabled for frontend integration