from sqlalchemy import Column, Integer, String, DateTime, func,ForeignKey,Boolean,Float
from app.db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
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

class ProjectProviderKey(Base):
    __tablename__ = "project_provider_keys"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False)

    encrypted_api_key = Column(String, nullable=False)
    meta_data = Column(String, nullable=True)    

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", backref="provider_keys")
    provider = relationship("Provider", backref="project_connections")

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)         
    category = Column(String, nullable=False)                  
    base_url = Column(String, nullable=True)                   
    logo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User_Roles(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)   
    roles_id = Column(Integer,ForeignKey('roles.id',ondelete='CASCADE'),nullable=False)  

    user = relationship('User',backref='roles')
    roles = relationship('Role',backref='users')

class Api_Keys(Base):
    __tablename__ = 'api_keys'

    id = Column(Integer,primary_key=True,index=True)
    key_hash = Column(String,nullable=False)
    owner = Column(String,nullable=False)
    owner_type = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    project = relationship("Project", backref="api_keys")
    is_active = Column(Boolean, default=True) 
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    expires_at = Column(DateTime(timezone=True),nullable=False)   
    last_used_at = Column(DateTime(timezone=True),nullable=True)

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, nullable=False)
    path = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    ip = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE') ,nullable=False,index=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())    

    owner = relationship("User", backref="projects")

class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    service = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())






