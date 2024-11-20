import re
from typing import Union

def validate_user(username: str, email: str, user_id=None):
    if not isinstance(username, str): # Check if username is a string
        raise ValueError("Username must be a string.")
    
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not isinstance(email, str) or not re.match(email_regex, email): # Check if email is a string and validate it's format
        raise ValueError("Email must be a string or invalid email format.")
    
    if user_id is not None:
        if not user_id.isdigit() or int(user_id) <= 0: # Check if id is positive integer
            raise ValueError("Id must be a positive integer.")
        

def validate_user_column_name_value(column_name: str, column_value: Union[str, int]):
    if column_name not in ["id", "username", "email"]:
        raise ValueError("Invalid column name.")
    
    if column_name == "id":
        if column_value <= 0: # Check if id is positive integer
            raise ValueError("Id must be a positive integer.") 
    elif column_name == "username":
        if not isinstance(column_value, str): # Check if username is a string
            raise ValueError("Username must be a string.")   
    elif column_name == "email":
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not isinstance(column_value, str): # Check if email is a string
            raise ValueError("Email must be a string.")
        if not not re.match(email_regex, column_value): # Validate email format
            raise ValueError("Invalid email format.")
        