from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY as list
from database import Base

# ---- Modelos ----
class User(Base):
    __tablename__ = "users"

    user_name = Column(String)
    user_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    age = Column(Integer, nullable=True)
    recommendations = Column(list(String))
    zip = Column(Integer, nullable=True)