from typing import List

import uvicorn

from fastapi import FastAPI, Depends, HTTPException

from .database import db, models, schemas, queries
from sqlalchemy.ext.asyncio import AsyncSession

app: FastAPI = FastAPI(title="Project", docs_url="/")


@app.on_event("startup")
async def startup() -> None:
    await db.start_up(reset_tables=False)


@app.post("/users/", response_model=schemas.UserScheme)
async def create_user(
    user: schemas.UserScheme, session: AsyncSession = Depends(db.session.get_session)
) -> schemas.UserScheme:
    return await queries.create_user(user=user, session=session)


@app.get("/users/", response_model=List[schemas.UserScheme])
async def get_users(
    session: AsyncSession = Depends(db.session.get_session),
) -> List[schemas.UserScheme]:
    return await queries.get_all_users(session=session)


@app.get("/users/{user_id}/", response_model=schemas.UserScheme)
async def get_user(
    user_id: int, session: AsyncSession = Depends(db.session.get_session)
) -> schemas.UserScheme:
    user: schemas.UserScheme = await queries.get_user(user_id=user_id, session=session)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    return user


@app.put("/users/{user_id}/", response_model=schemas.UserScheme)
async def update_user(
    user_id: int,
    user_data: schemas.BaseUserScheme,
    session: AsyncSession = Depends(db.session.get_session)
) -> schemas.UserScheme:
    user: schemas.UserScheme = await queries.get_user(user_id=user_id, session=session)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    return await queries.update_user(
        user=user, user_data=user_data, session=session
    )


@app.delete("/users/{user_id}/")
async def delete_user(
    user_id: int, session: AsyncSession = Depends(db.session.get_session)
) -> str:
    user: schemas.UserScheme = await queries.get_user(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    await queries.delete_user(user, session=session)

    return f"User with id: {user.id} is deleted!"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
