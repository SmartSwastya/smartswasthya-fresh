from __future__ import annotations
from tools.obvious_router import auto_model
# â–‘â–ˆâ–€â–ˆâ–‘â–ˆâ–€â–„â–‘â–€â–ˆâ–€â–‘â–ˆâ–‘â–ˆâ–‘â–ˆâ–€â–„â–‘â–ˆâ–‘â–ˆâ–‘â–ˆâ–‘â–ˆâ–‘â–ˆâ–€â–€
# â–‘â–ˆâ–€â–ˆâ–‘â–ˆâ–‘â–ˆâ–‘â–‘â–ˆâ–‘â–‘â–ˆâ–‘â–ˆâ–‘â–ˆâ–€â–„â–‘â–ˆâ–‘â–ˆâ–‘â–‘â–ˆâ–‘â–‘â–€â–€â–ˆ
# â–‘â–€â–‘â–€â–‘â–€â–€â–‘â–‘â–€â–€â–€â–‘â–€â–€â–€â–‘â–€â–‘â–€â–‘â–€â–€â–€â–‘â–‘â–€â–‘â–‘â–€â–€â–€

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    from models.ele_devices import ElectronicDevice
    from models.bio_metrics import BioMetricDevice
    from models.user_login_history import UserLoginHistory
    from models.user_activity_log import UserActivityLog
    from models.user_wallet import UserWallet
    from models.user_kyc import UserKYC
    from models.user_devices import UserDevice
    from models.user_location_logs import UserLocationLog
    from models.appointments import Appointment
    from models.medical_records import MedicalRecord
    from models.family_health_status import FamilyHealthStatus
    from models.user_documents import UserDocument
    from models.health_insurance_profiles import HealthInsuranceProfile
#region auto_model
    from models.staff_attendance import StaffAttendance
    from models.order_service_tracking import OrderServiceTracking
    from models.notifications import Notification
    from models.feedbacks import Feedback
    from models.emergency_contacts import EmergencyContact
    from models.emergency_alerts import EmergencyAlert
    from models.referral_links import ReferralLink
    from models.referral_earnings import ReferralEarning
    from models.otp_sessions import OTPSession
    from models.chat_sessions import ChatSession
    from models.device_logs import DeviceLog
    from models.ambulance_profiles import AmbulanceProfile
    from models.blood_bank_profiles import BloodBankProfile
    from models.corporate_profiles import CorporateProfile
    from models.doctor_profiles import DoctorProfile
    from models.home_care_profiles import HomeCareProfile
    from models.hospital_profiles import HospitalProfile
    from models.lab_profiles import LabProfile
    from models.pharmacy_profiles import PharmacyProfile
    from models.billing_invoices import BillingInvoice
    from models.live_tracking import LiveTrackingLog
    from models.login_sessions import LoginSession
    from models.medication_reminders import MedicationReminder
    from models.message_logs import MessageLog
    from models.vendor_profiles import VendorPsrofile

# @auto_model
class User(Base):
    __tablename__ = "users"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    mobile = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    gender = Column(String, nullable=True)
    signup_source = Column(String, nullable=True)
    role = Column(String, default="smart_user")

    otp_sessions = relationship("models.otp_sessions.OTPSession", back_populates="user")
    login_history = relationship("models.user_login_history.UserLoginHistory", back_populates="user")
    user_activity_logs = relationship("models.user_activity_log.UserActivityLog", back_populates="user")
    wallet = relationship("models.user_wallet.UserWallet", uselist=False, back_populates="user")
    wallet_transactions = relationship("models.wallet_transactions.WalletTransaction", back_populates="user")
    kyc = relationship("models.user_kyc.UserKYC", uselist=False, back_populates="user")
    devices = relationship("models.user_devices.UserDevice", back_populates="user")
    location_logs = relationship("models.user_location_logs.UserLocationLog", back_populates="user")
    ele_devices = relationship("models.ele_devices.ElectronicDevice", back_populates="user")
    bio_metrics = relationship("models.bio_metrics.BioMetricDevice", back_populates="user")
    appointments = relationship("models.appointments.Appointment", back_populates="user")
    medical_records = relationship("models.medical_records.MedicalRecord", back_populates="user")
    prescriptions = relationship("models.prescriptions.Prescription", back_populates="user")
    family_health_status = relationship("models.family_health_status.FamilyHealthStatus", back_populates="user")
    user_documents = relationship("models.user_documents.UserDocument", back_populates="user")
    staff_attendance = relationship("models.staff_attendance.StaffAttendance", back_populates="user")
    order_service_tracking = relationship("OrderServiceTracking", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    emergency_contacts = relationship("EmergencyContact", back_populates="user")
    emergency_alerts = relationship("EmergencyAlert", back_populates="user")
    referral_links = relationship("models.referral_links.ReferralLink", back_populates="user")
    referral_earnings = relationship("models.referral_earnings.ReferralEarning", back_populates="user")
    ambulance_profile = relationship("models.ambulance_profiles.AmbulanceProfile", uselist=False, back_populates="user")
    blood_bank_profile = relationship("models.blood_bank_profiles.BloodBankProfile", uselist=False, back_populates="user")
    corporate_profile = relationship("models.corporate_profiles.CorporateProfile", uselist=False, back_populates="user")
    doctor_profile = relationship("models.doctor_profiles.DoctorProfile", uselist=False, back_populates="user")
    home_care_profile = relationship("models.home_care_profiles.HomeCareProfile", uselist=False, back_populates="user")
    hospital_profile = relationship("models.hospital_profiles.HospitalProfile", uselist=False, back_populates="user")
    lab_profile = relationship("models.lab_profiles.LabProfile", uselist=False, back_populates="user")
    pharmacy_profile = relationship("models.pharmacy_profiles.PharmacyProfile", uselist=False, back_populates="user")
    billing_invoices = relationship("models.billing_invoices.BillingInvoice", back_populates="user")
    chat_sessions = relationship("models.chat_sessions.ChatSession", back_populates="user")
    device_logs = relationship("models.device_logs.DeviceLog", back_populates="user")
    digital_signatures = relationship("models.digital_signatures.DigitalSignature", back_populates="user")
    health_insurance_profiles = relationship("HealthInsuranceProfile", back_populates="user")
    health_metrics = relationship("models.health_metrics.HealthMetric", back_populates="user")
    lab_test_results = relationship("models.lab_test_results.LabTestResult", back_populates="user")
    live_tracking_logs = relationship("models.live_tracking.LiveTrackingLog", back_populates="user")
    login_sessions = relationship("models.login_sessions.LoginSession", back_populates="user")
    medication_reminders = relationship("MedicationReminder", back_populates="user")
    message_logs = relationship("models.message_logs.MessageLog", back_populates="sender")
    otp_logs = relationship("OTPLog", back_populates="user")
    password_resets = relationship("PasswordResetRequest", back_populates="user")
    scan_reports = relationship("ScanReport", back_populates="user")
    service_requests = relationship("ServiceRequest", back_populates="user")
    support_tickets = relationship("SupportTicket", back_populates="user")
    user_consents = relationship("models.user_consents.UserConsent", back_populates="user")
    user_settings = relationship("models.user_settings.UserSetting", back_populates="user")
    vendor_profiles = relationship("models.vendor_profiles.VendorProfile", back_populates="user")





