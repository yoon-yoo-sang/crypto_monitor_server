import datetime
import enum

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Double, Enum
from sqlalchemy.types import JSON
from app.config.database import Base
target_metadata = Base.metadata


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Coin(BaseModel):
    __tablename__ = "coin"

    market = Column(String(100), nullable=False)
    korean_name = Column(String(200), nullable=False, unique=True)
    english_name = Column(String(200), nullable=False, unique=True)
    market_capitalization = Column(Integer, nullable=True)
    market_event_warning = Column(Boolean, nullable=False)
    market_event_caution = Column(JSON, nullable=False)


class CoinPriceHistoryChange(enum.Enum):
    EVEN = 'EVEN'
    RISE = 'RISE'
    FALL = 'FALL'


class CoinPriceHistory(BaseModel):
    __tablename__ = "coin_price_history"

    coin_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    change = Column(Enum(CoinPriceHistoryChange), nullable=False)
    change_price = Column(Double, nullable=False)
    change_rate = Column(Double, nullable=False)
    acc_trade_price_24h = Column(Double, nullable=False)


class CoinAnalysisHistory(BaseModel):
    __tablename__ = "coin_analysis_history"

    coin_id = Column(Integer, nullable=False)
    coin_history_id = Column(Integer, nullable=True)
    dopamine_index = Column(Double, nullable=False)
    rsi = Column(Double, nullable=False)
    macd = Column(Double, nullable=False)
