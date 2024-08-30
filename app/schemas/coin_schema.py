from pydantic import BaseModel


class CoinBase(BaseModel):
    market: str
    korean_name: str
    english_name: str
    market_event_warning: bool
    market_event_caution: dict


class CoinCreate(CoinBase):
    pass
