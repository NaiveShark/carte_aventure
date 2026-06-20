from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastcrud import FastCRUD
from sqladmin import Admin

from app.config import engine, Base, get_db
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate
from app.admin_views import ProductAdmin

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="FastCRUD UI Template", lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")

admin = Admin(app, engine, title="Admin Portal")
admin.add_view(ProductAdmin)

product_crud = FastCRUD(Product)
PAGE_SIZE = 5

@app.get("/")
async def list_products(request: Request, page: int = 1, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * PAGE_SIZE
    
    crud_data = await product_crud.get_multi(db=db, offset=offset, limit=PAGE_SIZE + 1)
    products_list = crud_data.get("data", [])
    
    has_next = len(products_list) > PAGE_SIZE
    display_products = products_list[:PAGE_SIZE]

    # FIX: Pass 'request' as the FIRST argument, template name SECOND, and context dictionary
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "products": display_products, 
            "page": page, 
            "has_next": has_next
        }
    )

@app.get("/products/new")
async def new_product_form(request: Request):
    # FIX: Pass 'request' as the FIRST argument
    return templates.TemplateResponse(
        request,
        "edit.html", 
        {"product": None}
    )

@app.post("/products/new")
async def create_product(
    name: str = Form(...), description: str = Form(None), 
    price: float = Form(...), in_stock: bool = Form(False), db: AsyncSession = Depends(get_db)
):
    schema_data = ProductCreate(name=name, description=description, price=price, in_stock=in_stock)
    await product_crud.create(db=db, object=schema_data)
    return RedirectResponse(url="/", status_code=303)

@app.get("/products/{product_id}/edit")
async def edit_product_form(request: Request, product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_crud.get(db=db, id=product_id)
    # FIX: Pass 'request' as the FIRST argument
    return templates.TemplateResponse(
        request,
        "edit.html", 
        {"product": product}
    )

@app.post("/products/{product_id}/edit")
async def update_product(
    product_id: int, name: str = Form(...), description: str = Form(None), 
    price: float = Form(...), in_stock: bool = Form(False), db: AsyncSession = Depends(get_db)
):
    schema_data = ProductUpdate(name=name, description=description, price=price, in_stock=in_stock)
    await product_crud.update(db=db, object=schema_data, id=product_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/products/{product_id}/delete")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    await product_crud.delete(db=db, id=product_id)
    return RedirectResponse(url="/", status_code=303)
