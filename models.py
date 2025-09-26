from sqlalchemy import Column, Integer, String
from sqlalchemy.types import JSON
from database import Base

# ---- Modelos ----
class User(Base):
    __tablename__ = "users"

    user_name = Column(String)
    user_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    age = Column(Integer, nullable=True)
    recommendations = Column(JSON)
    zip = Column(Integer, nullable=True)