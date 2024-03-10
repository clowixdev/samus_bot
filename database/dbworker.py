from typing import Any

from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, User, Template


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
        Session: session interface through which all queries will be executed
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
        user (User): An user entity
    """
    session = create_session(engine)
    rr_name = '_empty_name_'
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            user = User(id=user_id, username=username, rr_name=rr_name)
        else:
            rr_name = user.rr_name
        session.add(user)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return rr_name

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

def get_usernames(engine: Engine) -> list:
    """Generates list of all usernames and returns it

    Args:
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.

    Returns:
        list: List of all users stored in database
    """
    session = create_session(engine)
    usernames = []
    try:
        all_users = session.execute(select(User).order_by(User.id)).all()
        for user in all_users:
            usernames.append(user[0].username)
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return usernames

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

def get_templates(engine: Engine) -> dict:
    """Function, that will generate dictionary from database table with templates
    Args:
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    """
    session = create_session(engine)
    all_templates = dict()
    try:
        templates = session.execute(select(Template).order_by(Template.id)).all()
        for template in templates:
            all_templates[template[0].id] = (f"{template[0].template}")
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return all_templates

def update_templates(template: str, id: int, engine: Engine) -> None:
    """Function, that will update database table with templates after adding

    Args:
        template (str): Users message template
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.

    Returns:
        dict: dict of all templates stored in database
    """
    session = create_session(engine)
    try:
        db_template = session.query(Template).filter_by(id=id).first()
        if not db_template:
            db_template = Template(id=id, template=template)
        session.add(db_template)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()

def delete_template(template_id: int, engine: Engine) -> None:
    """Function that will delete template with matched template_id

    Args:
        template_id (int): ID of template that will be deleted
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    """
    session = create_session(engine)
    try:
        template = session.query(Template).filter_by(id=template_id).first()
        session.delete(template)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()