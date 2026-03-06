from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exam & Job Tracker API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Exam & Job Tracker API!"}

@app.post("/items", response_model=schemas.TrackedItemResponse)
def create_item(item: schemas.TrackedItemCreate, db: Session = Depends(get_db)):
    
    db_item = models.TrackedItem(**item.model_dump())
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item

@app.get("/items", response_model=List[schemas.TrackedItemResponse])
def get_all_items(
    status: Optional[str] = None, 
    category: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    
    query = db.query(models.TrackedItem)
    
    
    if status:
        query = query.filter(models.TrackedItem.status == status)
        
    
    if category:
        query = query.filter(models.TrackedItem.category == category)
        
   
    return query.all()

@app.put("/items/{item_id}", response_model=schemas.TrackedItemResponse)
def update_item(item_id: int, updated_item: schemas.TrackedItemCreate, db: Session = Depends(get_db)):
   
    db_item = db.query(models.TrackedItem).filter(models.TrackedItem.id == item_id).first()
    
   
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    
    db_item.title = updated_item.title
    db_item.category = updated_item.category
    db_item.status = updated_item.status
    db_item.notes = updated_item.notes
    
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
   
    db_item = db.query(models.TrackedItem).filter(models.TrackedItem.id == item_id).first()
    
    
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    
    db.delete(db_item)
    db.commit()
    
    return {"message": f"Item {item_id} successfully deleted"}