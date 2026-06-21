from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Auth and user tables
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Boolean, Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from starlette.requests import Request
from starlette_login.mixins import UserMixin


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    password = Column(String(128))
    is_admin = Column(Boolean, default=False)
    is_editor = Column(Boolean, default=False)

    @property
    def identity(self):
        return self.id

    @property
    def display_name(self) -> str:
        return ' '.join([self.first_name, self.last_name])

    def set_password(self, password: str):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password: str):
        return pbkdf2_sha256.verify(password, self.password)

    @classmethod
    async def get_user_by_id(cls, request: Request, user_id: int):
        db = request.state.db
        return await db.get(User, user_id)

    @classmethod
    async def get_user_by_username(cls, db: AsyncSession, username: str):
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        if result is None:
            return None
        else:
            return result.scalars().first()

    @classmethod
    async def create_user(
        cls, db: AsyncSession,
        username: str, password: str, 
        is_admin: bool = False,
        is_editor: bool = False
    ):
        user = cls(
            username=username,
            password=password,
            is_admin=is_admin,
            is_editor=is_editor
        )
        user.set_password(password)
        db.add(user)
        await db.commit()
        return user



# Data tables

class Quest(Base):
    __tablename__ = "quest"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    question_description = Column(String, nullable=True)
    quest_id: Mapped[int] = mapped_column(ForeignKey("quest.id"), nullable=False )
    quest = relationship( "Quest" )
    
    @property
    async def get_answers( cls ):
        db = request.state.db
        query = select(AnswerVar).where(AnswerVar.question_id == self.id)
        result = await db.execute(query)
        if result is None:
            return None
        else:
            return result.scalars().all()

class AnswerVar(Base):
    __tablename__ = "answervar"
    id = Column(Integer, primary_key=True, index=True)
    answer_title = Column(String, nullable=True)

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False )
    question = relationship( "Question" )

    right_message = Column(String, nullable=True)
    is_true_answer = Column(Boolean, default=True)
    wrong_message = Column(String, nullable=True)
