from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """SQLAlchemy model of user.

    Args:
        Base (Class): base class for declarative class definitions
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    rr_name = Column(String)
    crit_dmg = Column(Integer)
    uid = Column(Integer)
    platform = Column(String)
    forest_fraction = Column(Boolean)
    magic_fraction = Column(Boolean)
    light_fraction = Column(Boolean)
    tech_fraction = Column(Boolean)
    dark_fraction = Column(Boolean)

class Template(Base):
    """SQLAlchemy model of template

    Args:
        Base (Class): base class for declarative class definitions
    """
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    template = Column(String)