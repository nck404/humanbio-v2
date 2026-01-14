import os
import sys
from app import app, db, User

def create_admin():
    with app.app_context():
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        
        # Check if user exists
        user = User.query.filter((User.username == username) | (User.email == email)).first()
        
        if user:
            print(f"User {username} already exists. Promoting to admin...")
            user.is_admin = True
        else:
            print(f"Creating new admin user: {username}")
            user = User(username=username, email=email, is_admin=True)
            user.set_password(password)
            db.session.add(user)
        
        db.session.commit()
        print("Successfully updated admin status!")

if __name__ == "__main__":
    create_admin()
