import frappe
from frappe import _
from .response import res_error, res_success

@frappe.whitelist(allow_guest=True)
def register(email, full_name, password):
    if not email:
        return res_error("Email is required", "email", "REQUIRED")
    if not full_name:
        return res_error("Full name is required", "full_name", "REQUIRED")
    if not password:
        return res_error("Password is required", "password", "REQUIRED")
    if frappe.db.exists("User", email):
        return res_error(_("Email is already registered."))

    user = frappe.new_doc("User")
    user.email = email
    user.first_name = full_name
    user.enabled = 1
    user.send_welcome_email = 1
    user.new_password = password
  

    user.append("roles", {"role": "Website User"})

    user.flags.ignore_permissions = True
    user.insert()
    
    return res_success("User created successfully", {
        "user_id": user.name
    })
