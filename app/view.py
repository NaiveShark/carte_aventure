from urllib.parse import parse_qsl

from starlette.requests import Request
from starlette.responses import (
    HTMLResponse, PlainTextResponse, RedirectResponse
)
from starlette_login.decorator import login_required
from starlette_login.utils import login_user, logout_user

from .models import User, Quest

from starlette.templating import Jinja2Templates
from starlette_login.login_manager import LoginManager

from sqlalchemy import select
#, delete 

login_manager = LoginManager(redirect_to='login', secret_key='no_secret_here')
template = Jinja2Templates(directory='templates')


HOME_PAGE = """
You are logged in as {username}<br/>Links:
<ul>
    <li><a href="/">Home</a></li>
    <li><a href="/admin">Admin</a></li>
    <li><a href="/logout">Logout</a></li>
<ul>
"""
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
    
    quest_id = request.path_params['quest_id']
    quest = await db.get(Quest, quest_id )

#    fn = select(Node_Type_Product).where( Node_Type_Product.product_id == product_id, Node_Type_Product.out_flag == True )
#    from_nodes = session.execute( fn ).scalars().all()

#    tn = select(Node_Type_Product).where( Node_Type_Product.product_id == product_id, Node_Type_Product.out_flag == False )
#    to_nodes = session.execute( tn ).scalars().all()

    
    
    
 #   query = select(Quest).where(Quest.is_active == True )
 #   result = await db.execute(query)
    if quest is None:
        return None
    else:
        return template.TemplateResponse(
                 request,
                'play_quest.html', context={ 'quest' : quest, }
            )
           
 