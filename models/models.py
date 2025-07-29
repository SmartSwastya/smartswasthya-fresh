from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
#region auto_model
# ========================================================
# ðŸ“ SECTION: SQLAlchemy Model - Central Model Registry
# ðŸ”¹ Location: models/models.py
# ðŸ”¸ Purpose: Register all models for Alembic + Mapping
# ========================================================

import sys
import os
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.base import Base

# ========================================================
# ðŸ§¬ SECTION: Import All Models
# ========================================================

# Core User Models
from models.user_activity_log import UserActivityLog
from models.user_devices import UserDevice
from models.user_login_history import UserLoginHistory
from models.user_location_logs import UserLocationLog
from models.user_wallet import UserWallet
from models.referral_links import ReferralLink
from models.referral_earnings import ReferralEarning

# Authentication & Verification
from models.otp_sessions import OTPSession
from models.login_sessions import LoginSession
from models.otp_logs import OTPLog
from models.password_reset_requests import PasswordResetRequest

# Profiles (One-to-One)
from models.doctor_profiles import DoctorProfile
from models.pharmacy_profiles import PharmacyProfile
from models.lab_profiles import LabProfile
from models.ambulance_profiles import AmbulanceProfile
from models.home_care_profiles import HomeCareProfile
from models.corporate_profiles import CorporateProfile
from models.hospital_profiles import HospitalProfile
from models.blood_bank_profiles import BloodBankProfile

# Health Devices and Biometrics
from models.ele_devices import ElectronicDevice
from models.bio_metrics import BioMetricDevice

# Healthcare Services
from models.appointments import Appointment
from models.health_metrics import HealthMetric
from models.medical_records import MedicalRecord
from models.lab_test_results import LabTestResult
from models.medication_reminders import MedicationReminder
from models.family_health_status import FamilyHealthStatus
from models.live_tracking import LiveTrackingLog
from models.emergency_contacts import EmergencyContact
from models.emergency_alerts import EmergencyAlert

# Communication & Feedback
from models.chat_sessions import ChatSession
from models.message_logs import MessageLog
from models.notifications import Notification
from models.feedbacks import Feedback

# System Logs & Tracking
from models.device_logs import DeviceLog
from models.user_consents import UserConsent
from models.app_update_logs import AppUpdateLog

# Service & Support
from models.service_requests import ServiceRequest
from models.support_tickets import SupportTicket
from models.order_service_tracking import OrderServiceTracking

# Financial
from models.billing_invoices import BillingInvoice
from models.digital_signatures import DigitalSignature

# Vendor & Inventory
from models.vendor_profiles import VendorProfile
from models.staff_profiles import StaffProfile
from models.inventory_items import InventoryItem
from models.service_packages import ServicePackage

# Legal & Documents
from models.user_documents import UserDocument

# ========================================================
# ðŸ“Œ NOTE:
# - All models are auto-discovered by Alembic via import.
# - Ensure every new model is listed above.
# - Remove unused models explicitly from this file.
# ========================================================


if TYPE_CHECKING:
    from models.users import User
    
