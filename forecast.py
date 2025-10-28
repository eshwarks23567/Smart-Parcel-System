import os
import logging
from datetime import datetime, timedelta
from collections import Counter
import json

logger = logging.getLogger(__name__)


def _count_parcels_per_day(session):
    from models import Parcel
    rows = session.query(Parcel).filter(Parcel.arrival_time != None).all()
    dates = [p.arrival_time.date() for p in rows if p.arrival_time]
    counts = Counter(dates)
    # return list of tuples sorted by date
    items = sorted(counts.items())
    return items


def forecast_next_days(session, days=7):
    """Try to forecast next `days` parcel arrivals.

    If Prophet is installed, use it. Otherwise fall back to a simple moving average.
    Returns list of dicts: {date: iso, predicted: float}
    """
    items = _count_parcels_per_day(session)
    if not items:
        # no historical data, return zeros
        today = datetime.utcnow().date()
        return [{"date": (today + timedelta(days=i)).isoformat(), "predicted": 0.0} for i in range(1, days+1)]

    dates = [d for d, c in items]
    counts = [c for d, c in items]

    # Try Prophet
    try:
        from prophet import Prophet
        import pandas as pd
        df = pd.DataFrame({
            'ds': [pd.to_datetime(d) for d in dates],
            'y': counts
        })
        m = Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods=days)
        forecast = m.predict(future)
        preds = []
        for i in range(1, days+1):
            row = forecast.iloc[-i]
            date = pd.to_datetime(row['ds']).date()
            preds.append({
                'date': date.isoformat(),
                'predicted': float(max(0.0, row['yhat']))
            })
        preds = list(reversed(preds))
        return preds
    except Exception:
        logger.info('Prophet not available or failed; using moving average fallback')

    # Fallback: simple moving average of last 7 days (or available)
    window = min(7, len(counts))
    avg = sum(counts[-window:]) / float(window)
    today = datetime.utcnow().date()
    return [{"date": (today + timedelta(days=i)).isoformat(), "predicted": float(avg)} for i in range(1, days+1)]
