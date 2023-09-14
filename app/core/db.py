from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..main import get_settings


db_session = scoped_session(sessionmaker(bind=create_engine(get_settings().engine_url)))
