from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.auth import JWTBearer
from app.config.database import get_db
from app.services.coin_service import get_all_coins, get_coin_details, get_coin_histories
from app.schemas.coin_schema import CoinResponse, CoinDetailResponse, CoinHistoryResponse

router = APIRouter()


@router.get("/coins", response_model=list[CoinResponse], dependencies=[Depends(JWTBearer())])
async def list_coins(db: Session = Depends(get_db)):
    coins = get_all_coins(db)
    return coins


@router.get("/coins/{_id}", response_model=CoinDetailResponse, dependencies=[Depends(JWTBearer())])
async def coin_details(_id: int, db: Session = Depends(get_db)):
    try:
        return get_coin_details(_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/coins/{_id}/histories", response_model=list[CoinHistoryResponse], dependencies=[Depends(JWTBearer())])
async def coin_histories(_id: int, db: Session = Depends(get_db)):
    try:
        histories = get_coin_histories(_id, db)
        return histories
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
