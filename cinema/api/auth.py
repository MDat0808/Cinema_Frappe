import frappe
from frappe import _
from .response import res_error, res_success
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def register(email, full_name, password):
    if not email:
        return res_error("Email is required", "email", "REQUIRED")
    if not full_name:
        return res_error("Full name is required", "full_name", "REQUIRED")
    if not password:
        return res_error("Password is required", "password", "REQUIRED")
    if frappe.db.exists("User", email):
        return res_error("Email is already registered.", "email", "ALREADY_EXISTS")

    user = frappe.new_doc("User")
    user.email = email
    user.first_name = full_name
    user.enabled = 1
    user.send_welcome_email = 0
    user.new_password = password
  
    if not frappe.db.exists("Role", "User"):
        role_doc = frappe.get_doc({
            "doctype": "Role",
            "role_name": "User"
        })
        role_doc.flags.ignore_permissions = True
        role_doc.insert()


    user.append("roles", {"role": "User"})
    user.flags.ignore_permissions = True
    user.insert()
    
    return res_success("User created successfully", {
        "user_id": user.name
    })


@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = LoginManager()
        login_manager.authenticate(usr, pwd)
        login_manager.post_login()

        sid = frappe.session.sid
        user = frappe.session.user

        user_info = frappe.get_doc("User", user)

        return res_success("Login successful", {
                "sid": sid,
                "user": {
                    "name": user_info.name,
                    "full_name": user_info.full_name,
                    "email": user_info.email,
                    "roles": [r.role for r in user_info.get("roles", [])]
                }
        })
    except Exception as e:
        return res_error(f"Login failed: {str(e)}")