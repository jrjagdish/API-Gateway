from app.db.session import engine
from app.db.database import Base
from app.db.models import User

def init_db():
    Base.metadata.create_all(bind = engine)