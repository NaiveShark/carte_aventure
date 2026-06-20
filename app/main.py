from fastapi import FastAPI
from sqladmin import Admin
from app.config import engine, Base
from app.admin_views import UserAdmin

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Starter Kit")

# Set up SQLAdmin interface
admin = Admin(app, engine, title="Admin Dashboard")
admin.add_view(UserAdmin)

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI Starter App. Go to /admin for the dashboard."}
