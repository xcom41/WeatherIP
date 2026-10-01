from datetime import datetime

from sqlalchemy import (create_engine, Integer, String, Float, Date,
                        DateTime, select, engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    city: Mapped[str] = mapped_column(String)
    date: Mapped[datetime.date] = mapped_column(Date)
    temp_min: Mapped[float] = mapped_column(Float)
    temp_max: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    wind: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String)

def get_engine(url):
    return create_engine(url, future=True)

def init_db(engine):
    Base.metadata.create_all(engine)

def save_weather(engine, city, rows):
    i = 0
    with Session(engine) as session:
        for row in rows:
            exists = session.scalar(
                select(Weather).where(Weather.city == city, Weather.date == row["date"])
            )
            if exists:
                continue
            session.add(Weather(city=city, **row))
            i += 1
        session.commit()
    return i

def load_weather(engine, city):
    with Session(engine) as session:
        return list(
            session.scalars(
                select(Weather)
                .where(Weather.city == city)
                .order_by(Weather.date.desc())
                .limit(4)
            )
        )
