from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

from starlette.middleware.cors import CORSMiddleware


import models
from models import Threads, Comments
from database import engine, SessionLocal
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, DELETE, and PUT
    allow_headers=["*"],  # Adjust headers if needed
) # Allows which domains are allowed to interact with your API

models.Base.metadata.create_all(bind=engine) # Create all the tables

# metadata is an object that stores information about the table structures associated with the models (like column names, data types,
# relationships, etc. )

def get_db():
    db = SessionLocal() # Contact the database
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class ThreadRequest(BaseModel):
    title: str = Field(min_length=3)

class CommentRequest(BaseModel):
    content: str = Field(min_length=1)
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Threads).all()

@app.get("/thread/{thread_id}", status_code=status.HTTP_200_OK)
async def read_thread(db: db_dependency, thread_id: int = Path(gt=0)):
    thread_model = db.query(Threads).filter(Threads.id == thread_id).first()
    if thread_model is not None:
        return thread_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")

@app.post("/thread", status_code=status.HTTP_201_CREATED)
async def create_thread(db: db_dependency, thread_request: ThreadRequest):
    thread_model = Threads(**thread_request.model_dump())
    db.add(thread_model)
    db.commit()
    return thread_model

@app.put("/thread/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_thread(db: db_dependency, thread_request: ThreadRequest, thread_id: int = Path(gt=0)):
    thread_model = db.query(Threads).filter(Threads.id == thread_id).first()
    if thread_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")
    thread_model.title = thread_request.title

    db.add(thread_model)
    db.commit()

@app.delete("/thread/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thread(db: db_dependency, thread_id: int = Path(gt=0)):
    thread_model = db.query(Threads).filter(Threads.id == thread_id).first()
    if thread_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")
    # db.query(Threads).filter(Threads.id == thread_id).delete() # This querying through the data and deleting was causing problems
    db.delete(thread_model)
    db.commit()

@app.post("/thread/{thread_id}/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(db: db_dependency, thread_id: int, comment_request: CommentRequest):
    thread_model = db.query(Threads).filter(Threads.id == thread_id).first()
    if thread_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")

    comment_model = Comments(content=comment_request.content, thread_id=thread_id)
    db.add(comment_model)
    db.commit()
    db.refresh(comment_model)
    return comment_model

@app.get("/thread/{thread_id}/comments", status_code=status.HTTP_200_OK)
async def read_comments(db: db_dependency, thread_id: int = Path(gt=0)):
    thread_model = db.query(Threads).filter(Threads.id == thread_id).first()
    if thread_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")
    return thread_model.comments


@app.delete("/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(db: db_dependency, comment_id: int = Path(gt=0)):
    comment_model = db.query(Comments).filter(Comments.id == comment_id).first()
    if comment_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    db.delete(comment_model)
    db.commit()
    return {"message": "Comment deleted successfully"}

@app.put("/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_comment(db: db_dependency, comment_request: CommentRequest, comment_id: int = Path(gt=0)):
    comment_model = db.query(Comments).filter(Comments.id == comment_id).first()
    if comment_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    comment_model.content = comment_request.content
    db.add(comment_model)
    db.commit()
    return {"message": "Comment updated successfully"}