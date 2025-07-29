from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

# 📁 FILE: models/__init__.py
"""
Auto-import all model classes and expose them via __all__

✔ Uses Base from database.py
✔ Prevents re-declaration issues during hot reload
✔ Clean metadata access for Alembic or bootstrap tools
"""

# === Base Declaration ===
from models.base import Base  # Defined in database.py

# === Core Models ===
from .users import User
from .legacy_user import LegacyUser
from .user_profile_model import UserProfile
from .user_wallet import UserWallet
from .user_login_history import UserLoginHistory
from .user_location_logs import UserLocationLog
from .user_devices import UserDevice
from .user_documents import UserDocument
from .user_settings import UserSetting
from .user_kyc import UserKYC
from .user_activity_log import UserActivityLog
from .user_consents import UserConsent

# === Authentication & Security ===
from .otp_sessions import OTPSession
from .otp_logs import OTPLog
from .login_sessions import LoginSession
from .active_token import ActiveToken
from .password_reset_requests import PasswordResetRequest
from .digital_signatures import DigitalSignature

# === Health & Medical ===
from .medical_records import MedicalRecord
from .appointments import Appointment
from .prescriptions import Prescription
from .health_metrics import HealthMetric
from .lab_test_results import LabTestResult
from .notifications import Notification
from .feedbacks import Feedback
from .emergency_contacts import EmergencyContact
from .emergency_alerts import EmergencyAlert
from .family_health_status import FamilyHealthStatus
from .health_insurance_profiles import HealthInsuranceProfile
from .medication_reminders import MedicationReminder

# === Devices & Tracking ===
from .device_logs import DeviceLog
from .ele_devices import ElectronicDevice
from .bio_metrics import BioMetricDevice
from .live_tracking import LiveTrackingLog
from .chat_sessions import ChatSession

# === Institutional Profiles ===
from .doctor_profiles import DoctorProfile
from .hospital_profiles import HospitalProfile
from .lab_profiles import LabProfile
from .pharmacy_profiles import PharmacyProfile
from .ambulance_profiles import AmbulanceProfile
from .blood_bank_profiles import BloodBankProfile
from .home_care_profiles import HomeCareProfile
from .corporate_profiles import CorporateProfile
from .vendor_profiles import VendorProfile
from .staff_profiles import StaffProfile
from .staff_attendance import StaffAttendance

# === Operations & Transactions ===
from .wallet_transactions import WalletTransaction
from .billing_invoices import BillingInvoice
from .inventory_items import InventoryItem
from .inventory_transactions import InventoryTransaction
from .order_service_tracking import OrderServiceTracking
from .referral_earnings import ReferralEarning
from .referral_links import ReferralLink
from .service_requests import ServiceRequest
from .service_packages import ServicePackage
from .support_tickets import SupportTicket
from .message_logs import MessageLog

# === Task Tracker System ===
from .dev_tasks import DevTask
from .task_tracker.code_snippet_map import CodeSnippetMap
from .task_tracker.dev_assignment_log import DevAssignmentLog
from .task_tracker.model_trace import ModelTrace
from .task_tracker.route_trace import RouteTrace
from .task_tracker.task_master import TaskMaster
from .task_tracker.task_status_history import TaskStatusHistory

# === Other Utilities ===
from .app_update_logs import AppUpdateLog
from .scan_reports import ScanReport

# === Exported Objects ===
__all__ = [
    "Base", "User", "LegacyUser", "UserProfile", "UserWallet", "UserLoginHistory",
    "UserLocationLog", "UserDevice", "UserDocument", "UserSetting", "user_kyc",
    "UserActivityLog", "UserConsent", "OTPSession", "OTPLog", "LoginSession",
    "ActiveToken", "PasswordResetRequest", "DigitalSignature", "MedicalRecord",
    "Appointments", "Prescriptions", "HealthMetric", "LabTestResult", "Notification",
    "Feedbacks", "EmergencyContact", "EmergencyAlert", "FamilyHealthStatus",
    "DeviceLog", "ElectronicDevice", "BioMetricDevice", "LiveTrackingLog",
    "ChatSession", "DoctorProfile", "HospitalProfile", "LabProfile", "PharmacyProfile",
    "AmbulanceProfile", "BloodBankProfile", "HomeCareProfile", "CorporateProfile",
    "VendorProfile", "StaffProfile", "StaffAttendance", "WalletTransaction",
    "BillingInvoice", "InventoryItem", "InventoryTransaction", "OrderServiceTracking",
    "ReferralEarning", "ReferralLink", "ServiceRequest", "ServicePackage",
    "SupportTicket", "MessageLog", "DevTask", "CodeSnippetMap", "DevAssignmentLog",
    "ModelTrace", "RouteTrace", "TaskMaster", "TaskStatusHistory", "AppUpdateLog",
    "ScanReport"
]
