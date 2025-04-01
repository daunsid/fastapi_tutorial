from distutils.command.build import build
from webbrowser import get
from .app.utils import hashed
from tkinter import SE
from turtle import title
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from .app import schema
from random import randrange
import psycopg2
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
import time
from .app import model
from .app.database import engine, SessionLocal, get_db
from .routers import post, users, auth
model.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres",
        password="password", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successfull")
        break
    except Exception as error:
        print("connecting to database failed")
        print('Error: ', error)
        time.sleep(2)


my_posts = [
    {"title": "title of posts 1", "content": "content of posts", "id":1},
    {"title":"fav food","content": "I like pazza", "id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
