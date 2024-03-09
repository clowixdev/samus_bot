from typing import Any

from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, User


def create_db_engine() -> Engine:
    """Function that creates sqlalchemy engine to create sessions.

    Returns:
        engine: An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    """
    engine = create_engine('sqlite+pysqlite:///database/database.db')
    Base.metadata.create_all(engine)

    return engine


def create_session(engine: Engine) -> Session:
    """Function that creates sessions to interact with database.

    Args:
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.

    Returns:
        _type_: _description_
    """
    Session = sessionmaker(bind=engine)
    return Session()


def get_user(user_id: int, username:str, engine: Engine) -> User:
    """Function that return a user if he exists in the database; otherwise, it creates it.

    Args:
        user_id (int): ID of user thah defined by Telegram
        username (str): username of user that is defined by user and could be changed
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.

    Returns:
        user (User): _description_
    """
    session = create_session(engine)
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            user = User(id=user_id, username=username, rr_name='')
            session.add(user)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return user

def add_rr_name(user_id: int, username:str, ingame_name: str, engine: Engine) -> User:
    """Function that adds rush royale username for user.

    Args:
        user_id (int): ID of user thah defined by Telegram
        username (str): username of user that is defined by user and could be changed
        ingame_name (str): username in rush royale
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    """
    session = create_session(engine)
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.rr_name = ingame_name
            session.add(user)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def gen_users(engine: Engine) -> list:
    """Generates list of all users and returns it

    Args:
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.

    Returns:
        list: List of all users stored in database
    """
    session = create_session(engine)
    users = []
    try:
        all_users = session.execute(select(User).order_by(User.id)).all()
        for user in all_users:
            users += user
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return users