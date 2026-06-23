from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Auth and user tables
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Boolean, Column, Integer, String, DateTime, select
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
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

class Question(Base):
    id = Column(Integer, primary_key=True, index=True)
    question_title = Column(String, nullable=True)
    quest_id: Mapped[int] = mapped_column(ForeignKey("quest.id"), nullable=False )
    quest = relationship( "Quest" )

class AnswerVar(Base):
    id = Column(Integer, primary_key=True, index=True)
    answer_title = Column(String, nullable=True)

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False )
    question = relationship( "Question" )

    right_message = Column(String, nullable=True)
    is_true_answer = Column(Boolean, default=False, nullable=False )
    wrong_message = Column(String, nullable=True)

# quest played by player
class Player_Quest(Base):
    id = Column(Integer, primary_key=True, index=True)

    quest_id: Mapped[int] = mapped_column(ForeignKey("quest.id"), nullable=False )
    quest = relationship( "Quest" )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False )
    user = relationship( "User" )

    quest_began = Column( DateTime, nullable=False )
    quest_end = Column( DateTime(timezone=True) )
    
    questions_count = Column(Integer, nullable=False, default=0 )
    answered_count = Column(Integer, nullable=False, default=0 )
    answered_right_count = Column(Integer, nullable=False, default=0 )
    answered_wrong_count = Column(Integer, nullable=False, default=0 )
    final_score = Column(Integer, nullable=False, default=0 )
    
# quest played by player
class Player_Quest_Answers(Base):
    id = Column(Integer, primary_key=True, index=True)
    player_quest_id: Mapped[int] = mapped_column(ForeignKey("player_quest.id"), nullable=False )
    player_quest = relationship( "Player_Quest" )
    answered_dt = Column( DateTime )
    
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False )
    question = relationship( "Question" )
    
    answervar_id: Mapped[int] = mapped_column(ForeignKey("answervar.id"), nullable=False )
    answervar = relationship( "AnswerVar" )
    
    is_right_answer = Column(Boolean, nullable=False )
    
    

#