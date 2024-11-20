from typing import Union, TypeVar, List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta
from database.models import User, Product, Order, OrderProduct
from database.database import get_session, Base
from utils.validation import validate_user, validate_user_column_name_value

# Define a generic type for SQLAlchemy models
T = TypeVar('T', bound=DeclarativeMeta)

# Map strings to SQLAlchemy model classes
model_mapping = {
    "user": User,
    "order": Order,
    "product": Product,
    "order_product": OrderProduct
}

    
""" DEMONSTRATE CREATE FUNCTIONS """
def create_user(username: str, email: str) -> User:
    validate_user(username=username, email=email) # Validate passed values
    session = get_session() # Get SQLAlchemy session

    try:
        user = User(username=username, email=email) # Create User object

        session.add(user)
        session.commit()

        return(user) # Return created User object
    
    except SQLAlchemyError as e: # Generic SQLALchemy error
        session.rollback()
        raise Exception(f"SQLAlchemyError: {str(e)}")
    
    except Exception as e: # Generic exception
        session.rollback()
        raise Exception(f"Unexpected error: {str(e)}")
    
    finally:
        session.close()


def create_product(name: str, price: float, description: str) -> Product:
    pass


def create_order(user_id: int, total_amount: float) -> Order:
    pass


def create_order_product(order_id: int, product_id: int, quantity: int) -> OrderProduct:
    pass


""" DEMONSTRATE GET FUNCTIONS """
def get_list_of_models(model_name: str) -> List[T]:
    model = model_mapping.get(model_name.lower()) # Get the model class based on the string input
    session = get_session() # Get SQLAlchemy session
    
    if not model:
        raise ValueError(f"Model '{model}' not found in mapping.")
    
    return session.query(model).all() # Return all records of the selected model


def get_user_by_column(column_name: str, column_value: Union[str, int]) -> User:
    validate_user_column_name_value(column_name=column_name, column_value=column_value) # Validate column name and value
    session = get_session() # Get SQLAlchemy session

    try:
        return session.query(User).filter(getattr(User, column_name) == column_value).first() # Return found user or None
    
    except SQLAlchemyError as e: # Generic SQLALchemy error
        raise Exception(f"SQLAlchemyError: {str(e)}")
    
    except Exception as e: # Generic error
        raise Exception(f"Unexpected error: {str(e)}")
    
    finally:
        session.close()


def get_product_by_id(product_id: int):
    pass


def get_product_by_name(product_name: str):
    pass


def get_order_by_id(order_id: int):
    pass


""" DEMONSTRATE UPDATE FUNCTIONS """
def update_user(user_id: int, username: str, email: str) -> User:
    validate_user(username=username, email=email, user_id=user_id)   
    session = get_session() # Get SQLAlchemy session

    try:
        db_user = session.query(User).filter(User.id == user_id).first() # Try to find user by id
        if db_user: # Update user if found
            db_user.username = username
            db_user.email = email
            session.commit()
        return db_user # Return updated user or None

    except SQLAlchemyError as e: # Generic SQLALchemy error
        session.rollback()
        raise Exception(f"SQLAlchemyError: {str(e)}")
    
    except Exception as e: # Generic error
        session.rollback()
        raise Exception(f"Unexpected error: {str(e)}")
    
    finally:
        session.close()


def update_product(product_id: int, name: str, price: float, description: str) -> Product:
    pass


def update_order_status(order_id: int, status: str) -> Order:
    pass


""" DEMONSTRATE DELETE FUNCTIONS """
def delete_user_by_column(column_name: str, column_value: Union[str, int]):
    validate_user_column_name_value(column_name=column_name, column_value=column_value) # Validate column name and value
    session = get_session()

    try:
        db_user = session.query(User).filter(getattr(User, column_name) == column_value).first() # Return found user or None
        if db_user: # Delete user if found
            session.delete(db_user)
            session.commit()

    except SQLAlchemyError as e: # Generic SQLALchemy error
        session.rollback()
        raise Exception(f"SQLAlchemyError: {str(e)}")
    
    except Exception as e: # Generic exception
        session.rollback()
        raise Exception(f"Unexpected error: {str(e)}")
    
    finally:
        session.close()


def delete_product(product_id: int):
    pass
