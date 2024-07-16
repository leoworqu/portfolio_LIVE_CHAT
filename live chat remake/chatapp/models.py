from datetime import datetime
from chatapp import db, login_Manager
from flask_login import UserMixin

# Function to load a user by ID for flask_login
@login_Manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model representing users of the application
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}', '{self.city}', '{self.country}', '{self.about}' )"


