import os
import logging

try:
    from twilio.rest import Client
    _TWILIO_AVAILABLE = True
except Exception:
    _TWILIO_AVAILABLE = False

logger = logging.getLogger(__name__)


def send_sms(to_number: str, body: str) -> bool:
    """Send SMS using Twilio if credentials are present. Returns True on success or False otherwise.

    Environment variables:
    - TWILIO_ACCOUNT_SID
    - TWILIO_AUTH_TOKEN
    - TWILIO_FROM
    """
    sid = os.environ.get('TWILIO_ACCOUNT_SID')
    token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_FROM')

    if not sid or not token or not from_number:
        logger.info('Twilio credentials not configured; skipping SMS send. To enable, set TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN/TWILIO_FROM')
        logger.info('SMS to %s: %s', to_number, body)
        return False

    if not _TWILIO_AVAILABLE:
        logger.warning('twilio package not installed; cannot send SMS')
        return False

    try:
        client = Client(sid, token)
        message = client.messages.create(body=body, from_=from_number, to=to_number)
        logger.info('Sent SMS SID=%s', getattr(message, 'sid', ''))
        return True
    except Exception as e:
        logger.exception('Failed to send SMS: %s', e)
        return False
