import logging

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from sqladmin import Admin

from starlette_login.backends import SessionAuthBackend
from starlette_login.login_manager import LoginManager
from starlette_login.middleware import AuthenticationMiddleware

from .admin_views import UserAdmin, QuestAdmin, QuestionAdmin, AnswerVarAdmin
from .models import Base, User
from .view import login_page, logout_page, reg_new_user, home_page, view_user_profile, view_quiz_top, quests_page, view_quest, play_quest, in_play_quest, handle_qqa, map_tools, in_play_it_next
from .pop import pop_data, BOT_USER_NAME, BOT_USER_TITLE

import mimetypes
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('text/css', '.css')

SECRET_KEY = 'our_webapp_secret_key'
DB_URL = 'sqlite+aiosqlite:///./mq.db'

logger = logging.getLogger('uvicorn.error')
db_engine = create_async_engine(DB_URL, poolclass=NullPool)
LocalDBSession = sessionmaker(
    db_engine, class_=AsyncSession, expire_on_commit=False
)

login_manager = LoginManager(
    redirect_to='/login', secret_key=SECRET_KEY
)
login_manager.set_user_loader(User.get_user_by_id)

middleware = [
    Middleware(SessionMiddleware, secret_key=SECRET_KEY),
    Middleware(
        AuthenticationMiddleware,
        backend=SessionAuthBackend(login_manager),
        login_manager=login_manager,
        excluded_dirs=['/statics']
    )
]


app = FastAPI(
    middleware=middleware,
    routes=[
        Route('/', home_page, name='home'),
        Route('/quests', quests_page, name='quests_page'),
        Route('/view_quiz_top', view_quiz_top, name='view_quiz_top'),

        Route("/view/quest/{quest_id}", view_quest, name='view_quest'),
        Route("/quest/play_it/{quest_id}", play_quest, name='play_quest'),
        Route("/quest/in_play_it/{player_quest_id}", in_play_quest, name='in_play_quest'),
        Route("/quest/in_play_it_next/{player_quest_id}", in_play_it_next, name='in_play_it_next'),
        Route("/quest/submit_form-qqa/{player_quest_id}/{current_question_id}", handle_qqa, methods=["POST"]),

        Route('/profile', view_user_profile, name='view_user_profile'),
        Route('/reg_new_user', reg_new_user, methods=['GET', 'POST'], name='reg_new_user'),
        Route('/login', login_page, methods=['GET', 'POST'], name='login'),
        Route('/logout', logout_page, name='logout'),


        Route('/map_tools', map_tools, name='map_tools'),
        Mount("/statics", StaticFiles(directory="statics"), name="statics"),

    ]
)
app.state.login_manager = login_manager

# Use `SessionMiddleware` and `AuthenticationMiddleware`
# to secure admin pages
admin = Admin(app, db_engine, middlewares=middleware)
admin.add_view(UserAdmin)
admin.add_view(QuestAdmin )
admin.add_view(QuestionAdmin )
admin.add_view(AnswerVarAdmin )

@app.middleware('http')
async def extensions(request: Request, call_next):
    try:
        request.state.db = LocalDBSession()
        response = await call_next(request)
    except Exception as exc:
        logger.exception(exc)
        response = PlainTextResponse(f'error: {exc}')
    finally:
        return response


@app.on_event('startup')
async def startup():
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # create admin user
    db = LocalDBSession()
    if not await User.get_user_by_username(db, 'admin'):
        await User.create_user(
            db, 'admin', 'Admin', 'password', is_admin=True
        )

    if not await User.get_user_by_username(db, 'u'):
        await User.create_user(
            db, 'u', 'u user', 'u'
        )

    if not await User.get_user_by_username(db, BOT_USER_NAME ):
        await User.create_user(
            db,
            BOT_USER_NAME, BOT_USER_TITLE,
            'password',
            is_bot=True
        )

    await pop_data( db )
    await db_engine.dispose()
