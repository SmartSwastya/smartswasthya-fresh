
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import os
from dotenv import load_dotenv
load_dotenv()

# auto_template
api_key = os.getenv("FAST2SMS_KEY")
sender_id = os.getenv("FAST2SMS_SENDER_ID", "SAMYAP")

if not api_key:
    raise ValueError("❌ FAST2SMS_API_KEY is missing in your .env file")

templates = {
    "AftBkgDtP": {
        "template_id": "180327",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, your appointment with {#var#} is confirmed for {#var#} at {#var#}. Patient ID: {#var#} - SAMYAP",
        "sample_content": "Dear Mr Hrushikesh Date, your appointment with Dr Ashwath Date is confirmed for Routine checkup at 13 Feb 17:30 PM. Patient ID: 123456 - SAMYAP"
    },
    "AftBkgPtD": {
        "template_id": "180328",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, new appointment booked with {#var#} on {#var#} at {#var#}. Patient ID: {#var#} - SAMYAP",
        "sample_content": "Dear Dr Ashwath Date, new appointment booked with Mr Hrushikesh Date on Routine checkup at 13 Feb 17:30 PM. Patient ID: 123456 - SAMYAP"
    },
    "OrderCancelled": {
        "template_id": "180329",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Your order ID {#var#} has been cancelled on {#var#}. For further assistance, contact Smart Swasthya Seva. - SAMYAP",
        "sample_content": "Dear Mr Hrushikesh Date, Your order ID 123456 has been cancelled on 13 Feb at 17:30 PM. - SAMYAP"
    },
    "PaymentConfirmedPatient": {
        "template_id": "180330",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Your payment for order ID {#var#} is confirmed on {#var#}. Team Samya Prabh - SAMYAP",
        "sample_content": "Dear Mr Hrushikesh Date, Your payment for order ID 123456 is confirmed on 13 Feb 17:30 PM. - SAMYAP"
    },
    "OrderCancelledVendor": {
        "template_id": "180331",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Order ID {#var#} assigned to you has been cancelled on {#var#}. Please check your dashboard. - SAMYAP",
        "sample_content": "Dear Dr Ashwath Date, Order ID 123456 cancelled. - SAMYAP"
    },
    "OrderConfirmedVendor": {
        "template_id": "180332",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, A new order ID {#var#} has been confirmed for you on {#var#}. Please check your dashboard. - SAMYAP",
        "sample_content": "Dear Dr Ashwath Date, A new order ID 123456 confirmed. - SAMYAP"
    },
    "OrderConfirmedPatient": {
        "template_id": "180333",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Your order ID {#var#} has been confirmed on {#var#}. Thank you for choosing Smart Swasthya Seva. - SAMYAP",
        "sample_content": "Dear Mr Hrushikesh Date, Order ID 123456 confirmed. - SAMYAP"
    },
    "PaymentCancelledPatient": {
        "template_id": "180334",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Your payment for order {#var#} was cancelled on {#var#}. Team Samya Prabh - SAMYAP",
        "sample_content": "Dear Mr Hrushikesh Date, Payment for order 123456 cancelled. - SAMYAP"
    },
    "PaymentCancelledVendor": {
        "template_id": "180335",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Payment for order ID {#var#} was cancelled on {#var#}. Check dashboard. - SAMYAP",
        "sample_content": "Dear Dr Ashwath Date, Payment for order ID 123456 was cancelled. - SAMYAP"
    },
    "AppointmentCancelledPatient": {
        "template_id": "180336",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Your appointment for order ID {#var#} has been cancelled on {#var#}. Team Samya Prabh - SAMYAP",
        "sample_content": "Appointment cancelled for Order 123456. - SAMYAP"
    },
    "AppointmentCancelledVendor": {
        "template_id": "180337",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Appointment for order ID {#var#} was cancelled on {#var#}. Check dashboard. - SAMYAP",
        "sample_content": "Vendor appointment cancelled. - SAMYAP"
    },
    "RegOTP": {
        "template_id": "180338",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Your OTP for completing registration on Smart Swasthya Seva is {#var#} Do not share it with anyone Team Samya Prabh - SAMYAP",
        "sample_content": "OTP: 123456. - SAMYAP"
    },
    "PaymentConfirmedVendor": {
        "template_id": "180339",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Payment for order ID {#var#} has been successfully processed on {#var#}. - SAMYAP",
        "sample_content": "Vendor payment success. - SAMYAP"
    },
    "ServiceCancellingVendor": {
        "template_id": "180660",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, booking for {#var#} with {#var#} on {#var#} has been cancelled. - SAMYAP",
        "sample_content": "Booking cancelled. - SAMYAP"
    },
    "ServiceCancelling": {
        "template_id": "180659",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, your booking for {#var#} with {#var#} on {#var#} has been cancelled. - SAMYAP",
        "sample_content": "Cancelled booking. - SAMYAP"
    },
    "ServiceBookingVedor": {
        "template_id": "180658",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, booking for {#var#} with {#var#} has been confirmed at {#var#}. - SAMYAP",
        "sample_content": "Confirmed vendor booking. - SAMYAP"
    },
    "ServiceBooking": {
        "template_id": "180657",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, your booking for {#var#} with {#var#} has been confirmed at {#var#}. - SAMYAP",
        "sample_content": "Confirmed booking. - SAMYAP"
    },
    "ForgotPassword": {
        "template_id": "181204",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, Your OTP to reset the password for Smart Swasthya Seva is {#var#}. Do not share it with anyone. Team Samya Prabh - SAMYAP",
        "sample_content": "OTP for password reset: 123456 - SAMYAP"
    },
    "OrderCompletion": {
        "template_id": "181282",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, your order ID {#var#} has been successfully completed. Team Samya Prabh - SAMYAP",
        "sample_content": "Order 123456 completed. - SAMYAP"
    },
    "OrderAcceptance": {
        "template_id": "181283",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, your order ID {#var#} has been successfully accepted. Team Samya Prabh - SAMYAP",
        "sample_content": "Order 123456 accepted. - SAMYAP"
    },
    "OrderCancellation": {
        "template_id": "181284",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, your order ID {#var#} has been successfully canceled. Team Samya Prabh - SAMYAP",
        "sample_content": "Order 123456 cancelled. - SAMYAP"
    },
    "OrderStatus": {
        "template_id": "181290",
        "sender_id": sender_id,
        "api_key": api_key,
        "sms_template": "Dear {#var#}, your order ID {#var#} has been successfully {#var#}. Team Samya Prabh - SAMYAP",
        "sample_content": "Order status: success. - SAMYAP"
    }
}

