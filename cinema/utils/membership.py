import frappe

def is_current_user_member():
    user = frappe.session.user
    return frappe.db.exists("Membership", {"user": user, "status": "Active"})
