from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.schemas.schemas import TakeNote, UpdateNote, UserResponse
from src.models.models import Notes
from src.database import get_db
from src.core.auth import get_current_user

route = APIRouter(
    tags=["Note"]
)


@route.get('/checknote/{id}')
async def check_note(id: str, 
                     db: AsyncSession = Depends(get_db),  
                     current_user: UserResponse = Depends(get_current_user)
                     ):
    result = await db.execute(select(Notes).where(Notes.note_id == id, Notes.owner_id == current_user.user_id))
    checked_note = result.scalars().first()
    if not checked_note:
        raise HTTPException(
            status_code=404, 
            detail="Note not found"
            )
    return checked_note


@route.put('/updatenote/{id}')
async def update_note(id: str, 
                      update_request: UpdateNote, 
                      db: AsyncSession = Depends(get_db), 
                      current_user: UserResponse = Depends(get_current_user)
                      ) -> dict:
    result = await db.execute(select(Notes).where(Notes.note_id == id, Notes.owner_id == current_user.user_id))
    note = result.scalars().first()
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found !"
        )
    for key, value in update_request.dict().items():
        setattr(note, key, value)
    await db.commit() 
    await db.refresh(note)
    return {"message": "Note Updated Successfully !"}


@route.delete('/deletenote/{id}')
async def delete_note(id, 
                      db: AsyncSession = Depends(get_db), 
                      current_user: UserResponse = Depends(get_current_user)
                      ) -> dict:
    result = await db.execute(select(Notes).where(Notes.note_id == id, Notes.owner_id == current_user.user_id))
    note = result.scalars().first()
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found !"
        )
    await db.delete(note)
    await db.commit()
    return {"message": "Product Deleted !"}


@route.post('/takenote')
async def take_note(note: TakeNote, 
                    db: AsyncSession = Depends(get_db), 
                    current_user: UserResponse = Depends(get_current_user)
                    ):
    new_note = Notes(owner_id=current_user.user_id, note_title=note.note_title, note_content=note.note_content)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note