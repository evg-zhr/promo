from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import func


from app.db import Base, User, Reaction, SessionLocal, engine, ReactionSchema, ReactionResult, CreateUser


app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(engine)

@app.on_event("shutdown")
def shutdown_event():
    pass
    # Base.metadata.drop_all(engine)

def get_db():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()


@app.post("/login")
async def login(data: CreateUser, db = Depends(get_db)):
    user = db.query(User).where(User.name == data.name).first()    
    if user is None:
        user = User(name=data.name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

@app.get("/leaders")
async def get_leaders(limit: int = 50, db = Depends(get_db)) -> list[ReactionSchema]:
    return db.query(User.id, User.name, func.min(Reaction.time).label('time')).join(User, User.id == Reaction.user_id).group_by(User.id, User.name).order_by(Reaction.time.asc()).limit(limit).all()


@app.post("/reactions")
async def save_reactions(data: ReactionResult, db = Depends(get_db)):
    reaction = Reaction(**data.dict())
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction