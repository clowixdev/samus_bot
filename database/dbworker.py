from typing import Any, List

from sqlalchemy import create_engine, select, insert
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
    try:
        if user_id != None:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return None
        else:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return None

        session.expunge(user)
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return user


def add_user(userdata: list, engine: Engine) -> User:
    """Function that adds user with all attributes.

    Args:
        userdata (list): Stored data about player (format: [player_id, playername, username, critdmg, uid, platform, [fractions]]) 
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    """
    session = create_session(engine)
    try:
        user = User(
            id=userdata[0], 
            username=userdata[2], 
            rr_name=userdata[1],
            crit_dmg=userdata[3], 
            uid=userdata[4], 
            platform=userdata[5], 
            forest_fraction=0 in userdata[6],
            magic_fraction=1 in userdata[6],
            light_fraction=2 in userdata[6],
            tech_fraction=3 in userdata[6],
            dark_fraction=4 in userdata[6]
        )
        session.add(user)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def delete_user(user_id: int, engine: Engine) -> None:
    """Deletes user from database

    Args:
        user_id (int): ID of user thah defined by Telegram
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    """

    session = create_session(engine)
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return 
        session.delete(user)
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


def get_fraction_usernames(fraction: str, engine: Engine) -> list:
    """Generates list of usernames with needed fractions and returns it

    Args:
        fraction (str): Fraction that will be mentioned
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.

    Returns:
        list: List of users that was choosen
    """
    session = create_session(engine)
    usernames = []
    users = []
    try:
        match fraction:
            case fraction if fraction in ["Лесной союз 🍃", "/forest"]:
                users = session.execute(select(User).filter(User.forest_fraction.is_(True))).all()
            case fraction if fraction in ["Магический совет 🔮", "/magic"]:
                users = session.execute(select(User).filter(User.magic_fraction.is_(True))).all()
            case fraction if fraction in ["Королевство света ☀️", "/light"]:
                users = session.execute(select(User).filter(User.light_fraction.is_(True))).all()
            case fraction if fraction in ["Техногенное общество 💡","/tech"]:
                users = session.execute(select(User).filter(User.tech_fraction.is_(True))).all()
            case fraction if fraction in ["Тёмные владения 🦇", "/dark"]:
                users = session.execute(select(User).filter(User.dark_fraction.is_(True))).all()

        for user in users:
            usernames.append(user[0].username)
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return usernames


def gen_users(engine: Engine) -> list[User]:
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


def get_templates(engine: Engine) -> Template:
    """Function, that will return all Template objects
    Args:
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    
    Returns:
        Template: Template object
    """
    session = create_session(engine)
    templates = []
    try:
        all_templates = session.execute(select(Template).order_by(Template.id)).all()
        for template in all_templates:
            templates += template
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return templates


def get_templates_descriptions(engine: Engine) -> dict:
    """Function, that will generate dictionary from database table with templates descriptions
    Args:
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    
    Returns:
        dict: dict of all templates descriptions stored in database
    """
    session = create_session(engine)
    all_descriptions = dict()
    try:
        templates = session.execute(select(Template).order_by(Template.id)).all()
        for id, template in enumerate(templates):
            all_descriptions[id] = (f"{template[0].description}")
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    return all_descriptions


def add_templates(template: str, photos: List[bytes], description: str, engine: Engine) -> None:
    """Function, that will update database table with templates after adding

    Args:
        template (str): Users message template
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    """
    session = create_session(engine)
    try:
        template_obj = Template(template=template, description=description)

        if 0 < len(photos) and photos[0] is not None:
            template_obj.photo1 = photos[0]
        if 1 < len(photos) and photos[1] is not None:
            template_obj.photo2 = photos[1]
        if 2 < len(photos) and photos[2] is not None:
            template_obj.photo3 = photos[2]
        if 3 < len(photos) and photos[3] is not None:
            template_obj.photo4 = photos[3]
        if 4 < len(photos) and photos[4] is not None:
            template_obj.photo5 = photos[4]

        session.add(template_obj)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def delete_template(template: str, engine: Engine) -> None:
    """Function that will delete template with matched template text

    Args:
        template_id (str): text of template that will be deleted
        engine (Engine): An _engine.Engine object is instantiated publicly using the ~sqlalchemy.create_engine function.
    """
    session = create_session(engine)
    try:
        template = session.query(Template).filter_by(template=template).first()
        session.delete(template)
        session.commit()
    except BaseException as e:
        print(e)
        session.rollback()
    finally:
        session.close()