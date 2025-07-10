from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.schemas.schemas import TakeNote, UpdateNote, UserCreate
from app.models.models import Notes
from app.database import get_db
from app.utils.auth import get_current_user

route = APIRouter(
    tags=["Note"]
)


@route.get('/checknote/{id}')
def check_note(id: str, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    checked_note = db.query(Notes).filter(Notes.note_id == id).first()
    if not checked_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return checked_note


@route.put('/updatenote/{id}')
def update_note(id: str, update_request: UpdateNote, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    note = db.query(Notes).filter(Notes.note_id == id).first()
    if not note:
        pass
    for key, value in update_request.dict().items():
        setattr(note, key, value)
    db.commit() 
    db.refresh(note)
    return "Note Updated Successfully !"


@route.delete('/deletenote/{id}')
def delete_note(id, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    db.query(Notes).filter(Notes.note_id == id).delete(synchronize_session=False)
    db.commit()
    return "Product Deleted !"


@route.post('/takenote')
def take_note(note: TakeNote, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_user)):
    new_note = Notes(owner_id=note.owner_id, note_title=note.note_title, note_content=note.note_content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note