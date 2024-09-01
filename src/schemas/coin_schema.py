from datetime import datetime

from pydantic import BaseModel


class CoinBase(BaseModel):
    market: str
    korean_name: str
    english_name: str
    market_event_warning: bool
    market_event_caution: dict


class CoinCreate(CoinBase):
    pass


class CoinResponse(BaseModel):
    id: int
    market: str
    korean_name: str
    change: str
    change_rate: float
    current_price: float
    dopamine_index: float
    acc_trade_price_24h: float


class CoinDetailResponse(BaseModel):
    id: int
    market: str
    name: str
    market_event_warning: bool
    market_event_caution: dict
    acc_trade_price_24h: float
    histories: dict


class CoinHistoryResponse(BaseModel):
    price: float
    timestamp: datetime
    change: str
    change_price: float
    change_rate: float
    dopamine_index: float
    rsi: float
    macd: float
