# 📁 routes/popup_routes.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from tools.obvious_router import auto_route
from handler import auto_model, auto_logic
from tools.smart_template import templates
from tools.auth import get_current_user_optional
from database import get_db


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Setup                          ║
# ╚════════════════════════════════════════════════╝
router = APIRouter(prefix="/popup", tags=["Popups"])


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Individual Popup Routes               ║
# ╚════════════════════════════════════════════════╝

@auto_model
@auto_route
@auto_logic
@router.get("/appointments")
def appointments_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/appointments_popup.html", {"request": request, "appointments": user.appointments})


@auto_model
@auto_route
@auto_logic
@router.get("/popups")
def popups_view(request: Request):
    return templates.TemplateResponse("popups/popups.html", {"request": request})


@auto_model
@auto_route
@auto_logic
@router.get("/family-health-status")
def family_health_status_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/family_health_status_popup.html", {"request": request, "family": user.family_members})


@auto_model
@auto_route
@auto_logic
@router.get("/live-tracking")
def live_tracking_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/live_tracking_popup.html", {"request": request, "live_data": user.live_tracking})


@auto_model
@auto_route
@auto_logic
@router.get("/lab-report")
def lab_report_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/lab_report_popup.html", {"request": request, "reports": user.lab_reports})


@auto_model
@auto_route
@auto_logic
@router.get("/emergency-contact")
def emergency_contact_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/emergency_contact_popup.html", {"request": request, "contacts": user.emergency_alerts.emergency_contacts})


@auto_model
@auto_route
@auto_logic
@router.get("/health-tip")
def health_tip_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/health_tip_popup.html", {"request": request, "tip": user.daily_health_tips})


@auto_model
@auto_route
@auto_logic
@router.get("/billing-invoices")
def billing_invoices_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/billing_invoices_popup.html", {"request": request, "invoices": user.invoices})


@auto_model
@auto_route
@auto_logic
@router.get("/medical-history")
def medical_history_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/medical_history_popup.html", {"request": request, "history": user.medical_history})


@auto_model
@auto_route
@auto_logic
@router.get("/health-metrics")
def health_metrics_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/health_metrics_popup.html", {"request": request, "user": user})


@auto_model
@auto_route
@auto_logic
@router.get("/profile")
def profile_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/profile_popup.html", {"request": request, "user": user})


@auto_model
@auto_route
@auto_logic
@router.get("/feedback")
def feedback_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/feedback_popup.html", {"request": request, "user": user})


@auto_model
@auto_route
@auto_logic
@router.get("/staff-attendance")
def staff_attendance_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/staff_attendance_popup.html", {"request": request, "user": user})


@auto_model
@auto_route
@auto_logic
@router.get("/order-tracking")
def order_service_tracking_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/order_service_tracking_popup.html", {"request": request, "user": user})


@auto_model
@auto_route
@auto_logic
@router.get("/prescriptions")
def prescription_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/prescription_popup.html", {"request": request, "user": user})


@auto_model
@auto_route
@auto_logic
@router.get("/notifications")
def notifications_popup_view(request: Request, user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("popups/notifications_popup.html", {"request": request, "user": user})
