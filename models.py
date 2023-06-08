from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from database import engine

Base = declarative_base()


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    logo_image_url = Column(String)
    title = Column(String)
    card_details_id = Column(Integer, ForeignKey("card_details.id"), nullable=True)

    card_details = relationship("CardDetails", backref=backref("card", uselist=False), foreign_keys=[card_details_id])
class CardDetails(Base):
    __tablename__ = "card_details"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    details = Column(String)
    picture = Column(String, nullable=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    # card = relationship("Card", back_populates="card_details", foreign_keys=[card_id])

Base.metadata.create_all(bind=engine)