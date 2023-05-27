from curses import echo
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Double
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase, Mapped, mapped_column


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    reactions: Mapped[list["Reaction"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Reaction(Base):
    __tablename__ = "reaction"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[float]

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="reactions")



class CreateUser(BaseModel):
    name: str

class ReactionSchema(BaseModel):
    id: int
    name: str
    time: float

    class Config:
        orm_mode = True

class ReactionResult(BaseModel):
    user_id: int
    time: float