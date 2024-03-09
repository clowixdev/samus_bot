from sqlalchemy import Column, Integer, String
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

class Template(Base):
    """SQLAlchemy model of template

    Args:
        Base (Class): base class for declarative class definitions
    """
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    template = Column(String)