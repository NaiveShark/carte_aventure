from urllib.parse import parse_qsl

from starlette.requests import Request
from starlette.responses import (
    HTMLResponse, PlainTextResponse, RedirectResponse
)
from starlette_login.decorator import login_required
from starlette_login.utils import login_user, logout_user
from datetime import datetime

from .models import User, Quest, Question, Player_Quest

from starlette.templating import Jinja2Templates
from starlette_login.login_manager import LoginManager

from sqlalchemy import select
#, delete

login_manager = LoginManager(redirect_to='login', secret_key='no_secret_here')
template = Jinja2Templates(directory='templates' )


LOGIN_PAGE = """
<h4>{error}<h4>
<form method="POST">
<label>username <input name="username"></label>
<label>Password <input name="password" type="password"></label>
<button type="submit">Login</button>
</form>
"""


async def login_page(request: Request):
    db = request.state.db
    error = ''
    if request.method == 'POST':
        body = (await request.body()).decode()
        data = dict(parse_qsl(body))
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            error = "Invalid username or password"
        else:
            user = await User.get_user_by_username(db, username)
            if user:
                if user.check_password(password) is True:
                    await login_user(request, user)
                    return RedirectResponse('/', status_code=302)
                else:
                    error = "Invalid password"
            else:
                error = "User not found"
    return HTMLResponse(LOGIN_PAGE.format(error=error))


async def logout_page(request: Request):
    if request.user.is_authenticated:
        content = 'Logged out'
        await logout_user(request)
    else:
        content = 'You not logged in'
    return PlainTextResponse(content)

async def home_page(request: Request):
    return template.TemplateResponse(
    request,
        'home.html', context={ }
    )

@login_required
async def quests_page(request: Request):
    # main.LocalDBSession
    db = request.state.db

    query = select(Quest).where(Quest.is_active == True )
    result = await db.execute(query)
    if result is None:
        return None
    else:
        quests = result.scalars().all()
        return template.TemplateResponse(
                 request,
                'quests.html', context={ 'quests' : quests, }
            )

@login_required
async def view_quest(request: Request):
    # main.LocalDBSession
    db = request.state.db
    user = request.user

    quest_id = request.path_params['quest_id']
    quest = await db.get(Quest, quest_id )

    if quest is None:
        return None
    else:

        # check - may be quest is already played by user
        pq_query = select(Player_Quest).where(Player_Quest.quest_id == quest_id, Player_Quest.user_id == user.id )
        pq_e = await db.execute(pq_query)
        pq = pq_e.scalar_one_or_none()

        return template.TemplateResponse(
                 request,
                'play_quest.html', context={ 'quest' : quest, "pq" : pq }
            )

@login_required
async def play_quest(request: Request):
    # main.LocalDBSession
    db = request.state.db

    user = request.user

    quest_id = request.path_params['quest_id']
    quest = await db.get(Quest, quest_id )

    if quest is None:
        return None
    else:
        # check - may be quest is already played by user
        pq_query = select(Player_Quest).where(Player_Quest.quest_id == quest_id, Player_Quest.user_id == user.id )
        pq_e = await db.execute(pq_query)
        pq = pq_e.scalar_one_or_none()
        if pq:
            print( 'ready' )
        else:
            pq = Player_Quest( quest_id = quest_id, user_id = user.id, quest_began = datetime.now() )
            db.add( pq )
            await db.commit()
            print( 'new' )

        return RedirectResponse(url='/quest/in_play_it/' + str( pq.id ) )

@login_required
async def in_play_quest(request: Request):
    # main.LocalDBSession
    db = request.state.db

    user = request.user

    player_quest_id = request.path_params['player_quest_id']
    player_quest = await db.get(Player_Quest, player_quest_id )


    if player_quest is None:
        return None
    else:
        quest_id = player_quest.quest_id
        quest = await db.get(Quest, quest_id )
        questions_q = select(Question).where( Question.quest_id == quest_id )
        questions = await db.execute( questions_q )

        return template.TemplateResponse(
                 request,
                'play_quest_stage.html', context={
                'quest' : quest,
                "questions" : questions.scalars().all()
                }
            )



#