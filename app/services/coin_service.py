from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.coin import CoinPriceHistory, CoinAnalysisHistory, Coin
from app.schemas.coin_schema import CoinResponse, CoinDetailResponse, CoinHistoryResponse


def get_all_coins(db: Session):
    latest_price_subquery = (
        db.query(
            CoinPriceHistory.coin_id,
            CoinPriceHistory.change,
            CoinPriceHistory.change_rate,
            CoinPriceHistory.price,
            CoinPriceHistory.acc_trade_price_24h
        )
        .filter(CoinPriceHistory.id.in_(
            db.query(func.max(CoinPriceHistory.id))
            .group_by(CoinPriceHistory.coin_id)
        ))
        .subquery()
    )

    latest_analysis_subquery = (
        db.query(
            CoinAnalysisHistory.coin_id,
            CoinAnalysisHistory.dopamine_index
        )
        .filter(CoinAnalysisHistory.id.in_(
            db.query(func.max(CoinAnalysisHistory.id))
            .group_by(CoinAnalysisHistory.coin_id)
        ))
        .subquery()
    )

    results = (
        db.query(
            Coin.id,
            Coin.market,
            latest_price_subquery.c.change,
            latest_price_subquery.c.change_rate,
            latest_price_subquery.c.price,
            latest_price_subquery.c.acc_trade_price_24h,
            latest_analysis_subquery.c.dopamine_index
        )
        .outerjoin(latest_price_subquery, Coin.id == latest_price_subquery.c.coin_id)
        .outerjoin(latest_analysis_subquery, Coin.id == latest_analysis_subquery.c.coin_id)
        .all()
    )

    coin_list = [
        CoinResponse(
            id=result.id,
            market=result.market,
            change=result.change,
            change_rate=result.change_rate,
            current_price=result.price,
            dopamine_index=result.dopamine_index,
            acc_trade_price_24h=result.acc_trade_price_24h
        )
        for result in results
    ]

    return coin_list


def get_coin_details(coin_id: int, db: Session) -> CoinDetailResponse:
    # 코인 정보 가져오기
    coin = db.query(Coin).filter(Coin.id == coin_id).first()
    if not coin:
        raise ValueError(f"Coin with ID {coin_id} not found")

    # 최신 CoinPriceHistory 가져오기
    latest_price_history = db.query(CoinPriceHistory).filter(CoinPriceHistory.coin_id == coin.id).order_by(
        desc(CoinPriceHistory.id)).first()

    # 최신 CoinAnalysisHistory 가져오기
    latest_analysis_history = db.query(CoinAnalysisHistory).filter(CoinAnalysisHistory.coin_id == coin.id).order_by(
        desc(CoinAnalysisHistory.id)).first()

    if not latest_price_history or not latest_analysis_history:
        raise ValueError(f"Price or Analysis history not found for Coin ID {coin_id}")

    # 응답 객체 생성
    return CoinDetailResponse(
        id=coin.id,
        market=coin.market,
        name=coin.korean_name,  # 또는 coin.english_name, 필요에 따라 선택
        market_event_warning=coin.market_event_warning,
        market_event_caution=coin.market_event_caution,
        acc_trade_price_24h=latest_price_history.acc_trade_price_24h,
        histories={
            "price": latest_price_history.price,
            "timestamp": latest_price_history.timestamp.isoformat(),
            "change": latest_price_history.change,
            "change_price": latest_price_history.change_price,
            "change_rate": latest_price_history.change_rate,
            "dopamine_index": latest_analysis_history.dopamine_index,
            "rsi": latest_analysis_history.rsi,
            "macd": latest_analysis_history.macd
        }
    )


def get_coin_histories(coin_id: int, db: Session) -> List[CoinHistoryResponse]:
    # 코인의 모든 가격 이력 가져오기
    histories = db.query(CoinPriceHistory).filter(CoinPriceHistory.coin_id == coin_id).order_by(desc(CoinPriceHistory.id)).all()

    # 분석 이력 가져오기
    analysis_histories = {a.coin_history_id: a for a in db.query(CoinAnalysisHistory).filter(CoinAnalysisHistory.coin_id == coin_id).all()}

    response = []
    for history in histories:
        analysis = analysis_histories.get(history.id)
        response.append(CoinHistoryResponse(
            price=history.price,
            timestamp=history.timestamp,
            change=history.change,
            change_price=history.change_price,
            change_rate=history.change_rate,
            dopamine_index=analysis.dopamine_index if analysis else 0,
            rsi=analysis.rsi if analysis else 0,
            macd=analysis.macd if analysis else 0
        ))

    return response
