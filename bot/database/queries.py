from config.database import db
from database.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(url=db.url)
DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def find_user_by_id(user_id: int) -> User | None:
    with DatabaseSession() as session:
        return session.query(User).filter_by(user_id=user_id).first()


def find_user_by_tg_id(tg_id: int) -> User | None:
    with DatabaseSession() as session:
        return session.query(User).filter_by(tg_id=tg_id).first()


def save_user(user_id: int, tg_id: int) -> User:
    with DatabaseSession() as session:
        if user := find_user_by_id(user_id):
            return user

        user = User(user_id=user_id, tg_id=tg_id)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
