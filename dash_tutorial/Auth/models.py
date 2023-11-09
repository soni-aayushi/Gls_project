from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50),  nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True) 
    refresh_token = Column(String(450), nullable=False)
    session_token = Column(String, index=True)
    status = Column(Boolean)
    created_date = Column(DateTime, default=func.now())

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    email = Column(String, primary_key=True)
    reset_token = Column(String)
    reset_token_expiry = Column(DateTime)