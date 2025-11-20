from app.db.session import engine
from app.db.database import Base
from app.db.models import User,Refresh_token,Role,User_Roles,Api_Keys

def init_db():
    Base.metadata.create_all(bind = engine)