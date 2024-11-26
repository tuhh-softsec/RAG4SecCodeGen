import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup (replace with your actual database URI)
DATABASE_URI = 'sqlite:///users.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(LargeBinary, nullable=False)

# Create tables
Base.metadata.create_all(engine)

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def insert_user(username, password):
    # Hash the password with a new salt
    hashed_password = hash_password(password)
    # Insert the username and hashed password into the database
    new_user = User(username=username, password_hash=hashed_password)
    session.add(new_user)
    session.commit()

def authenticate_user(username, password):
    # Retrieve the user from the database
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
        return True  # Authentication successful
    else:
        return False  # Authentication failed

# Example usage
# Prompt the user for a username and password
input_username = input("Enter your username: ")
input_password = input("Enter your password: ")

# Insert the user into the database
insert_user(input_username, input_password)

# Authenticate the user
if authenticate_user(input_username, input_password):
    print("Authentication successful!")
else:
    print("Authentication failed.")

