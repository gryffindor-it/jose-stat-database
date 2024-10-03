from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Stats(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True, index=True)
    stat_text = Column(String, index=True)

class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    game_text = Column(String, index=True)
    game_id = Column(Integer, ForeignKey('stats.id'))