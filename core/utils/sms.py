import logging
from decouple import config
import africastalking

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Africa’s Talking SDK
username = config('AFRICASTALKING_USERNAME', default='sandbox')  # Match .env key
api_key = config('AFRICASTALKING_API_KEY')  # Match .env key

africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_sms(phone_number, message):
    """
    Send an SMS to the given phone number.
    """
    try:
        response = sms.send(message, [phone_number])
        logger.info(f"SMS sent successfully to {phone_number}: {response}")
        return response
    except Exception as e:
        logger.error(f"Error sending SMS to {phone_number}: {str(e)}")
        return None