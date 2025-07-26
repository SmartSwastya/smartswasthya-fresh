from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import random
from flask_mail import Message
from database import mail

@auto_model
@auto_route
@auto_logic
def generate_otp():
    return str(random.randint(100000, 999999))

@auto_model
@auto_route
@auto_logic
def send_verification_email(email, otp):
    msg = Message(subject="Smart Swasthya Email Verification",
                  recipients=[email])
    msg.body = f"Your OTP for verifying your email is: {otp}"
    mail.send(msg)

