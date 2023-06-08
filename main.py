from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, Session, joinedload
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
from dotenv import load_dotenv
from database import SessionLocal, database
from models import Card, CardDetails
from schemas import CardInDB, CardCreate, CardDetailsInDB, CardDetailsCreate

load_dotenv()

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/Cards/", response_model=CardInDB)
async def create_card(card: CardCreate):
    query = Card.__table__.insert().values(**card.dict())
    last_record_id = await database.execute(query)

    if last_record_id is None:
        raise HTTPException(status_code=400, detail="Card could not be created")

    return {**card.dict(), "id": last_record_id}


@app.post("/CardDetails/", response_model=CardDetailsInDB)
async def create_card_details(card_details: CardDetailsCreate, db: Session = Depends(get_db)):
    # Fetch the card by title
    card_query = Card.__table__.select().where(Card.title == card_details.title)
    card = await database.fetch_one(card_query)

    # If the card does not exist, return an error
    if card is None:
        raise HTTPException(status_code=404, detail="Card with matching title not found")

    # Create new card details with the matched card_id
    new_card_detail = CardDetails(**card_details.dict(), card_id=card['id'])
    db.add(new_card_detail)
    db.commit()
    db.refresh(new_card_detail)

    # Assign the CardDetails id directly to the Card's card_details_id field
    update_query = Card.__table__.update().where(Card.id == card['id']).values(card_details_id=new_card_detail.id)
    await database.execute(update_query)

    return new_card_detail

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()},
    )


@app.get("/Cards/", response_model=List[CardInDB])
async def read_cards():
    try:
        query = Card.__table__.select()
        result = await database.fetch_all(query)

        if not result:
            raise HTTPException(status_code=404, detail="No cards found")

        return result
    except Exception as e:
        raise e


@app.get("/Cards/{card_id}", response_model=CardInDB)
async def read_card(card_id: int, db: Session = Depends(get_db)):
    card_query = db.query(Card).options(joinedload(Card.card_details)).filter(Card.id == card_id)
    card = card_query.first()

    if card is None:
        raise HTTPException(status_code=404, detail=f"Card with ID={card_id} not found")

    return card


@app.get("/CardDetails/", response_model=List[CardDetailsInDB])
async def read_card_details():
    query = CardDetails.__table__.select()
    result = await database.fetch_all(query)

    if not result:
        raise HTTPException(status_code=404, detail="No card details found")

    return result


@app.get("/CardDetails/{card_details_id}", response_model=CardDetailsInDB)
async def read_card_detail(card_details_id: int):
    query = CardDetails.__table__.select().where(CardDetails.id == card_details_id)
    result = await database.fetch_one(query)

    if result is None:
        raise HTTPException(status_code=404, detail=f"CardDetails with ID={card_details_id} not found")

    return result
