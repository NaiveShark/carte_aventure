from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastcrud import FastCRUD
from sqladmin import Admin

from app.config import engine, Base, get_db
from app.models import Quest
from app.schemas import QuestCreate, QuestUpdate
from app.admin_views import QuestAdmin, QuestionAdmin, AnswerVarAdmin, QuestQuestionAdmin

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="FastCRUD UI Template", lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")

admin = Admin(app, engine, title="Admin Portal")
admin.add_view(QuestAdmin)
admin.add_view(QuestionAdmin)
admin.add_view(AnswerVarAdmin)
admin.add_view(QuestQuestionAdmin)

quest_crud = FastCRUD(Quest)
PAGE_SIZE = 5

@app.get("/")
async def list_quests(request: Request, page: int = 1, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * PAGE_SIZE
    
    crud_data = await quest_crud.get_multi(db=db, offset=offset, limit=PAGE_SIZE + 1)
    quests_list = crud_data.get("data", [])
    
    has_next = len(quests_list) > PAGE_SIZE
    display_quests = quests_list[:PAGE_SIZE]

    # FIX: Pass 'request' as the FIRST argument, template name SECOND, and context dictionary
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "quests": display_quests, 
            "page": page, 
            "has_next": has_next
        }
    )

@app.get("/quests/new")
async def new_quest_form(request: Request):
    # FIX: Pass 'request' as the FIRST argument
    return templates.TemplateResponse(
        request,
        "edit_quest.html", 
        {"quest": None}
    )

@app.post("/quests/new")
async def create_quest(
    name: str = Form(...), description: str = Form(None), 
    #price: float = Form(...), 
    is_active: bool = Form(False), db: AsyncSession = Depends(get_db)
):
    schema_data = QuestCreate(name=name, description=description, is_active=is_active)
    await quest_crud.create(db=db, object=schema_data)
    return RedirectResponse(url="/", status_code=303)

@app.get("/quests/{quest_id}/edit")
async def edit_quest_form(request: Request, quest_id: int, db: AsyncSession = Depends(get_db)):
    quest = await quest_crud.get(db=db, id=quest_id)
    # FIX: Pass 'request' as the FIRST argument
    return templates.TemplateResponse(
        request,
        "edit_quest.html", 
        {"quest": quest}
    )

@app.post("/quests/{quest_id}/edit")
async def update_product(
    quest_id: int, name: str = Form(...), description: str = Form(None), 
    #price: float = Form(...), 
    is_active: bool = Form(False), db: AsyncSession = Depends(get_db)
):
    schema_data = QuestUpdate(name=name, description=description, is_active=is_active)
    await quest_crud.update(db=db, object=schema_data, id=quest_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/quests/{quest_id}/delete")
async def delete_quest(quest_id: int, db: AsyncSession = Depends(get_db)):
    await quest_crud.delete(db=db, id=quest_id)
    return RedirectResponse(url="/", status_code=303)
