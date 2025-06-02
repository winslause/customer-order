from django.conf import settings
import africastalking
import logging

logger = logging.getLogger(__name__)

def send_sms(phone_number, message):
    """Send SMS using Africa's Talking API."""
    try:
        africastalking.initialize(
            username=settings.AFRICASTALKING_USERNAME,
            api_key=settings.AFRICASTALKING_API_KEY
        )
        sms = africastalking.SMS
        response = sms.send(message, [phone_number])
        logger.info(f"SMS sent to {phone_number}: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to send SMS to {phone_number}: {e}")
        return None