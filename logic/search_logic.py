# 📁 File: smartswasthya/logic/search_logic.py
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function

def categorize_query(query: str):
    """
    Basic category recognizer — Can be enhanced with NLP later
    """
    q = query.lower()
    if any(x in q for x in ["doctor", "dr.", "physician", "mbbs", "bams"]):
        return "doctor"
    elif any(x in q for x in ["hospital", "clinic", "lab", "scan", "ambulance"]):
        return "facility"
    elif any(x in q for x in ["tablet", "capsule", "dose", "mg", "ml", "paracetamol", "medicine"]):
        return "medicine"
    else:
        return "info"

def mock_search_results(query: str):
    category = categorize_query(query)
    if category == "doctor":
        return [
            {"title": "Dr. Sneha Joshi – Cardiologist", "location": "Nashik", "rating": "4.9"},
            {"title": "Dr. Arjun Mehta – Diabetologist", "location": "Pune", "rating": "4.7"},
        ]
    elif category == "facility":
        return [
            {"title": "Swasthya Path Lab – 24x7", "location": "Pune", "rating": "4.6"},
            {"title": "Medilife Ambulance – Emergency", "location": "Mumbai", "rating": "4.8"},
        ]
    elif category == "medicine":
        return [
            {"title": "Paracetamol 500mg", "desc": "Used for fever, safe for children above 5 yrs"},
            {"title": "Dolo 650", "desc": "Fever + Pain relief, adult dosage: 650mg x 3/day"},
        ]
    else:
        return [
            {"title": "What to do after vaccine fever?", "desc": "Apply cold cloth, rest, hydrate."},
            {"title": "When is child teething normal?", "desc": "Usually 6–12 months age range."}
        ]
