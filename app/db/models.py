from sqlalchemy import Column, Integer, String, DateTime, func,ForeignKey,Boolean
from app.db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Refresh_token(Base):
    __tablename__ = 'refresh_token'
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)  
    refresh_token = Column(String,nullable=False)
    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)

    user = relationship("User",backref="refresh_tokens")

class Role(Base):
    __tablename__ = 'roles'

    id =Column( Integer,primary_key=True,index=True)
    name = Column(String,unique=True,nullable=False)

class User_Roles(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users',ondelete='CASCADE'),nullable=False)   
    roles_id = Column(Integer,ForeignKey('roles',ondelete='CASCADE'),nullable=False)  

    user = relationship('User',backref='roles')
    roles = relationship('Role',backref='users')

class Api_Keys(Base):
    __tablename__ = 'api_keys'

    id = Column(Integer,primary_key=True,index=True)
    key_hash = Column(String,nullable=False)
    owner = Column(String,nullable=False)
    owner_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True) 
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    expires_at = Column(DateTime(timezone=True),nullable=False)   
    last_used_at = Column(DateTime(timezone=True),nullable=False)




